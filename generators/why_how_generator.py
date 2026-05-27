# generators/why_how_generator.py

import random
from typing import List, Dict
from utils.concept_extractor import extract_concepts
from generators.t5_utils import t5_generate, tokenizer

# -----------------------------
# CONFIG
# -----------------------------
MAX_INPUT_TOKENS = 512
MAX_ATTEMPTS_PER_CONCEPT = 3
SEED = 42

random.seed(SEED)


# -----------------------------
# SAFE CONTEXT TRUNCATION
# -----------------------------
def truncate_context(context: str) -> str:
    tokens = tokenizer.encode(
        context,
        truncation=True,
        max_length=MAX_INPUT_TOKENS
    )
    return tokenizer.decode(tokens, skip_special_tokens=True)


# -----------------------------
# RULE-BASED VALIDATION
# -----------------------------
def is_valid_why_question(question: str, concept: str) -> bool:
    q = question.lower().strip()

    if not q.startswith(("why", "how")):
        return False

    if len(q.split()) < 6:
        return False

    if concept.lower() not in q:
        return False

    if "outside the context" in q:
        return False

    return True


# -----------------------------
# HYBRID WHY/HOW GENERATOR
# -----------------------------
def generate_why_how_questions(
    context: str,
    num_questions: int = 3
) -> List[Dict]:

    context = truncate_context(context)

    concepts = extract_concepts(context, top_k=25)

    questions = []
    used_concepts = set()
    used_questions = set()

    for item in concepts:

        if len(questions) >= num_questions:
            break

        concept = item["concept"].strip()

        if concept in used_concepts:
            continue

        # -----------------------------
        # RULE: ANALYSIS BLOOM ONLY
        # -----------------------------
        bloom_level = "Analysis"
        difficulty = "hard"

        # -----------------------------
        # CONTROLLED PROMPT
        # -----------------------------
        prompt = (
            "You are an expert educational question generator.\n\n"
            "TASK:\n"
            "Generate ONE analytical WHY or HOW question.\n\n"
            "STRICT RULES:\n"
            "- Use ONLY the given context\n"
            "- Do NOT introduce new information\n"
            "- The question MUST be answerable from the context\n"
            "- The question MUST start with Why or How\n"
            "- The question MUST explicitly mention the concept\n\n"
            f"Concept: {concept}\n\n"
            f"Context:\n{context}\n\n"
            "Question:"
        )

        # -----------------------------
        # LLM GENERATION WITH RETRIES
        # -----------------------------
        generated_question = None

        for _ in range(MAX_ATTEMPTS_PER_CONCEPT):

            candidate = t5_generate(
                prompt=prompt,
                max_length=48,
                bloom_level=bloom_level
            ).strip()

            if is_valid_why_question(candidate, concept):
                generated_question = candidate
                break

        if not generated_question:
            continue

        if generated_question in used_questions:
            continue

        # -----------------------------
        # ACCEPT QUESTION
        # -----------------------------
        questions.append({
            "question": generated_question,
            "concept": concept,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "source": "flan-t5 + rules"
        })

        used_concepts.add(concept)
        used_questions.add(generated_question)

    return questions
