# generators/true_false_generator.py

import random
import re
from typing import List, Dict

from utils.concept_extractor import extract_concepts
from utils.postprocess import clean_question_text

random.seed(42)

# -------------------------------
# Filters
# -------------------------------

BAD_START_WORDS = {
    "refers",
    "enables",
    "includes",
    "allows",
    "helps",
    "these",
    "many",
    "several",
    "often"
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

    words = concept.split()

    if len(words) > 3:
        return False

    if words[0] in BAD_START_WORDS:
        return False

    return True


# -------------------------------
# Safe Word Replacement
# -------------------------------

def replace_whole_word(
    sentence: str,
    old: str,
    new: str
):

    pattern = r"\b" + re.escape(old) + r"\b"

    return re.sub(
        pattern,
        new,
        sentence,
        count=1,
        flags=re.IGNORECASE
    )


# -------------------------------
# Create False Statement
# -------------------------------

def create_false_statement(
    sentence: str,
    correct_concept: str,
    concepts: List[str]
):

    if correct_concept.lower() not in sentence.lower():
        return sentence

    wrong_choices = [

        c for c in concepts

        if (
            c.lower() != correct_concept.lower()
            and len(c.split()) <= 3
        )
    ]

    if not wrong_choices:
        return sentence

    wrong_concept = random.choice(
        wrong_choices
    )

    false_sentence = replace_whole_word(
        sentence,
        correct_concept,
        wrong_concept
    )

    if false_sentence == sentence:
        return sentence

    return false_sentence


# -------------------------------
# Generate True/False Questions
# -------------------------------

def generate_true_false(
    context: str,
    num_questions: int,
    target_blooms: List[str] = None,
    target_difficulty: List[str] = None,
    bloom_distribution: Dict[str, int] = None  # ✅ ADDED
) -> List[Dict]:
    concept_data = extract_concepts(
        context,
        top_k=40
    )

    concepts = [

        item["concept"]

        for item in concept_data

        if is_clean_concept(
            item["concept"]
        )
    ]

    questions: List[Dict] = []

    used_sentences = set()

    # -------------------------------
    # PRIMARY GENERATION
    # -------------------------------

    for item in concept_data:

        if len(questions) >= num_questions:
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

        sentence = sentences[0].strip()

        if len(sentence.split()) < 6:
            continue

        normalized = sentence.lower()[:80]

        if normalized in used_sentences:
            continue

        is_true = random.choice(
            [True, False]
        )

        if is_true:

            statement = sentence

        else:

            statement = create_false_statement(
                sentence,
                concept,
                concepts
            )

        question_text = statement.strip()

        if not question_text.endswith("?"):
            question_text += " (True/False)?"

        question_text = clean_question_text(
            question_text
        )

        questions.append({

            "question": question_text,

            "answer": str(is_true),

            # ML WILL PREDICT
            "bloom_level": None,

            "difficulty": None,

            "type": "true_false"

        })

        used_sentences.add(
            normalized
        )

    # -------------------------------
    # FALLBACK SAFETY
    # -------------------------------

    while len(questions) < num_questions:

        fallback_concept = random.choice(
            concepts
        )

        fallback_question = (

            f"{fallback_concept} is used in cybersecurity systems "

            "(True/False)?"

        )

        questions.append({

            "question": fallback_question,

            "answer": "True",

            # ML WILL PREDICT
            "bloom_level": None,

            "difficulty": None,

            "type": "true_false"

        })

    return questions[:num_questions]