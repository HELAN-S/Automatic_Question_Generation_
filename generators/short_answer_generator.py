# generators/short_answer_generator.py

import random
import re
import traceback
from typing import List, Dict

from utils.concept_extractor import extract_concepts
from utils.postprocess import clean_question_text
from generators.t5_utils import t5_generate, build_short_question_prompt

random.seed(42)

# -------------------------------
# Concept Filtering
# -------------------------------

BAD_CONCEPTS = {"helps", "allows", "often", "many"}

def is_clean_concept(concept: str):
    if not concept:
        return False
    c = str(concept).lower().strip()
    if len(c) < 3 or len(c.split()) > 3:
        return False
    if c in BAD_CONCEPTS:
        return False
    return True

# -------------------------------
# Answer Extraction
# -------------------------------

def extract_answer_from_context(concept: str, context: str):
    """
    Extract a one-sentence, concept-specific answer.
    Uses T5 first, fallback to regex-based sentence extraction.
    """
    clean_ctx = " ".join(context.split())
    try:
        prompt = (
            f"Context: {clean_ctx}\n\n"
            f"Task: Define '{concept}' in exactly one sentence. "
            f"The answer must be clear, concept-specific, and start with '{concept} is' or '{concept} refers to'."
        )
        answer = t5_generate(prompt)
        if answer and concept.lower() in answer.lower() and len(answer.split()) > 5:
            return answer.strip().split('.')[0] + "."
    except:
        pass

    # Regex fallback: take the first sentence containing the concept
    sentences = re.split(r'(?<=[.!?]) +', clean_ctx)
    for sent in sentences:
        if concept.lower() in sent.lower():
            return sent.strip().split('.')[0] + "."
    
    # Concept-specific generic fallback
    return f"{concept.capitalize()} is an important concept in cybersecurity mentioned in the context."

# -------------------------------
# Question Construction
# -------------------------------

def construct_question(concept: str, bloom: str):
    templates = {
        "Remember": [f"What is {concept}?", f"Define {concept}."],
        "Understand": [f"Explain the purpose of {concept}.", f"How would you describe {concept}?"],
        "Apply": [f"How is {concept} implemented?", f"Provide an example of {concept}."],
        "Analyze": [f"Why is {concept} significant?", f"Analyze the importance of {concept}."],
        "Evaluate": [f"Explain the effectiveness of {concept}.", f"Critique the role of {concept}."],
        "Create": [f"Explain how {concept} contributes to a new security strategy."]
    }
    return random.choice(templates.get(bloom, [f"Explain {concept}."]))

# -------------------------------
# Main Generator
# -------------------------------

def generate_short_questions(
    context: str,
    num_questions: int,
    target_blooms: List[str] = None,
    target_difficulty: str = "Medium",
    bloom_distribution: Dict[str, int] = None
) -> List[Dict]:

    try:
        concept_data = extract_concepts(context, top_k=40)
        concepts = [c["concept"] for c in concept_data if is_clean_concept(c["concept"])]

        if not concepts:
            return []

        # Build bloom selection pool
        bloom_pool = []
        if bloom_distribution:
            for level, count in bloom_distribution.items():
                bloom_pool.extend([level] * int(count))
        if not bloom_pool:
            bloom_pool = target_blooms if target_blooms else ["Remember"]

        final_questions = []
        used_answers = set()
        total_to_gen = min(num_questions, len(concepts))

        for i in range(total_to_gen):
            concept = concepts[i]
            bloom = bloom_pool[i % len(bloom_pool)]

            q_text = construct_question(concept, bloom)
            ans_text = extract_answer_from_context(concept, context)

            # Ensure unique answers
            if ans_text in used_answers:
                ans_text += f" (specific to {concept})"
            used_answers.add(ans_text)

            final_questions.append({
                "question": clean_question_text(q_text),
                "answer": ans_text,
                "bloom_level": bloom,
                "difficulty": target_difficulty,
                "type": "short_answer"
            })

        # Fallback: generate more if needed
        while len(final_questions) < num_questions:
            concept = random.choice(concepts)
            bloom = random.choice(bloom_pool)
            q_text = construct_question(concept, bloom)
            ans_text = extract_answer_from_context(concept, context)
            if ans_text in used_answers:
                ans_text += f" (specific to {concept})"
            used_answers.add(ans_text)
            final_questions.append({
                "question": clean_question_text(q_text),
                "answer": ans_text,
                "bloom_level": bloom,
                "difficulty": target_difficulty,
                "type": "short_answer"
            })

        return final_questions[:num_questions]

    except Exception as e:
        print(f"Generator Error: {e}")
        traceback.print_exc()
        return []