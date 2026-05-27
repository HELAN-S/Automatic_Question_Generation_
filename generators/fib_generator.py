# generators/fib_generator.py

import random
import re
from typing import List, Dict

from utils.concept_extractor import extract_concepts

random.seed(42)

# -------------------------------
# Filters
# -------------------------------

BAD_START_WORDS = {
    "refers", "enables", "includes", "allows",
    "helps", "often", "these", "many",
    "several", "various", "build", "make"
}


# -------------------------------
# Concept Cleaning
# -------------------------------

def is_clean_concept(
    concept: str
):

    concept = concept.lower().strip()

    if len(concept) < 4:
        return False

    if len(concept.split()) > 3:
        return False

    for w in BAD_START_WORDS:

        if concept.startswith(w):
            return False

    return True


# -------------------------------
# Replace Whole Word Only
# -------------------------------

def replace_whole_word(
    sentence: str,
    concept: str
):

    pattern = r"\b" + re.escape(concept) + r"\b"

    replaced = re.sub(
        pattern,
        "_____",
        sentence,
        count=1,
        flags=re.IGNORECASE
    )

    return replaced


# -------------------------------
# Create Blank Safely
# -------------------------------

def create_blank(
    sentence: str,
    concept: str
):

    if concept.lower() not in sentence.lower():
        return None

    new_sentence = replace_whole_word(
        sentence,
        concept
    )

    if new_sentence == sentence:
        return None

    if new_sentence.count("_____") != 1:
        return None

    if new_sentence.startswith("_____"):
        return None

    word_count = len(sentence.split())

    if word_count < 6:
        return None

    if word_count > 30:
        return None

    if not new_sentence.endswith("?"):
        new_sentence += "?"

    return new_sentence


# -------------------------------
# Main FIB Generator
# -------------------------------

def generate_fib(
    context: str,
    max_questions: int,
    target_blooms: List[str] = None,
    target_difficulty: List[str] = None,
    bloom_distribution: Dict[str, int] = None  # ✅ ADDED
) -> List[Dict]:
    concept_data = extract_concepts(
        context,
        top_k=50
    )

    fibs: List[Dict] = []

    used_pairs = set()

    # -------------------------------
    # PRIMARY GENERATION
    # -------------------------------

    for item in concept_data:

        if len(fibs) >= max_questions:
            break

        concept = item["concept"].strip()

        if not is_clean_concept(concept):
            continue

        sentences = item.get(
            "sentences",
            []
        )

        if not sentences:
            continue

        for sentence in sentences:

            if len(fibs) >= max_questions:
                break

            sentence = sentence.strip().rstrip(".")

            key = (
                concept.lower(),
                sentence.lower()[:80]
            )

            if key in used_pairs:
                continue

            question_text = create_blank(
                sentence,
                concept
            )

            if not question_text:
                continue

            fibs.append({

                "question": question_text,

                "answer": concept,

                # ML WILL PREDICT
                "bloom_level": None,

                "difficulty": None,

                "type": "fib"

            })

            used_pairs.add(key)

    # -------------------------------
    # FALLBACK SAFETY
    # -------------------------------

    clean_concepts = [

        item["concept"]

        for item in concept_data

        if is_clean_concept(
            item["concept"]
        )
    ]

    while len(fibs) < max_questions:

        fallback_concept = random.choice(
            clean_concepts
        )

        fallback_question = (

            f"{fallback_concept} is commonly used in cybersecurity systems _____?"

        )

        fibs.append({

            "question": fallback_question,

            "answer": fallback_concept,

            # ML WILL PREDICT
            "bloom_level": None,

            "difficulty": None,

            "type": "fib"

        })

    return fibs[:max_questions]