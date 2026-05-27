# generators/mcq_generator.py
import random
import re
from typing import List, Dict
from utils.concept_extractor import extract_concepts

random.seed(42)


# -----------------------------
# Clean and format sentence
# -----------------------------
def clean_sentence(text: str):
    text = text.replace("\n", " ").strip()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Fix joined sentences
    text = re.sub(r"\.(?=[A-Z])", ". ", text)

    return text


# -----------------------------
# Trim long sentences (NO "...") ❌
# -----------------------------
def trim_sentence(text: str, max_words=25):
    words = text.split()

    if len(words) <= max_words:
        return text

    return " ".join(words[:max_words])  # ✅ NO "..."


# -----------------------------
# Get best definition sentence
# -----------------------------
def get_definition_sentence(sentences, concept):
    for s in sentences:

        s = clean_sentence(s)
        s = trim_sentence(s)

        if concept.lower() in s.lower():

            word_count = len(s.split())

            # Keep only good length sentences
            if 8 <= word_count <= 25:
                return s

    return None


# -----------------------------
# Generate distractors (SMART)
# -----------------------------
def generate_distractors(concept, concept_data):

    distractors = []

    for item in concept_data:
        other = item["concept"]

        if other.lower() != concept.lower():
            distractors.append(other)

    distractors = list(set(distractors))
    random.shuffle(distractors)

    return distractors[:3]


# -----------------------------
# Bloom Question Templates
# -----------------------------
def build_question(concept, bloom):

    stems = {

        "Remember": [
            f"What is {concept}?",
            f"Which of the following defines {concept}?",
            f"Identify the correct meaning of {concept}."
        ],

        "Understand": [
            f"Which statement best explains {concept}?",
            f"What is the purpose of {concept}?",
            f"How is {concept} used in the given context?"
        ],

        "Apply": [
            f"How would you apply {concept} in practice?",
            f"Which scenario best demonstrates {concept}?",
            f"How can {concept} be implemented effectively?"
        ],

        "Analyze": [
            f"Which of the following best analyzes {concept}?",
            f"What are the key components of {concept}?",
            f"How does {concept} differ from related concepts?"
        ],

        "Evaluate": [
            f"Which option best evaluates {concept}?",
            f"Why is {concept} important in this context?",
            f"What is the best justification for {concept}?"
        ],

        "Create": [
            f"How would you design a solution using {concept}?",
            f"Which scenario requires creating a solution based on {concept}?",
            f"How can {concept} be used to develop a new approach?"
        ]
    }

    return random.choice(stems.get(bloom, stems["Remember"]))


# -----------------------------
# Bloom Plan Builder
# -----------------------------
def build_bloom_plan(target_blooms, distribution, total):

    plan = []

    if distribution:
        for bloom, count in distribution.items():
            if count > 0:
                plan.extend([bloom] * count)

    while len(plan) < total:
        plan.append(random.choice(target_blooms if target_blooms else ["Remember"]))

    return plan[:total]


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def generate_mcq(
    context: str,
    num_questions: int,
    target_blooms: List[str] = None,
    target_difficulty: str = "Medium",
    bloom_distribution: Dict[str, int] = None
) -> List[Dict]:

    concept_data = extract_concepts(context, top_k=50)

    if not concept_data:
        return []

    bloom_plan = build_bloom_plan(
        target_blooms,
        bloom_distribution,
        num_questions
    )

    questions = []
    used_answers = set()

    for i, data in enumerate(concept_data):

        if len(questions) >= num_questions:
            break

        concept = data["concept"]
        sentences = data.get("sentences", [])

        # -----------------------------
        # Correct Answer
        # -----------------------------
        answer = get_definition_sentence(sentences, concept)

        if not answer or answer in used_answers:
            continue

        # -----------------------------
        # Higher Bloom Fix (IMPORTANT)
        # -----------------------------
        bloom = bloom_plan[len(questions)]

        if bloom in ["Apply", "Analyze", "Evaluate", "Create"]:
            answer = f"{concept} is used to improve system functionality and security."

        # -----------------------------
        # Distractors
        # -----------------------------
        distractors = generate_distractors(concept, concept_data)

        if len(distractors) < 3:
            continue

        options = distractors + [answer]
        random.shuffle(options)

        # -----------------------------
        # Final Question
        # -----------------------------
        questions.append({

            "question": build_question(concept, bloom),

            "options": options,

            "answer": answer,

            "bloom_level": bloom,

            "difficulty": target_difficulty,

            "type": "mcq"

        })

        used_answers.add(answer)

    return questions