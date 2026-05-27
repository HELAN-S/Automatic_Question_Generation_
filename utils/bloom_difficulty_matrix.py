# utils/bloom_difficulty_matrix.py

BLOOM_DIFFICULTY_MAP = {
    "remember": ["easy"],
    "understand": ["easy", "medium"],
    "apply": ["medium"],
    "analyze": ["medium", "hard"],
    "evaluate": ["hard"],
    "create": ["hard"]
}
from utils.predictors import predict_and_postprocess
import re

def postprocess_question(q: dict):
    """
    Replace placeholder predictions with ML-driven predictions.
    Updates question dict in place.
    """
    result = predict_and_postprocess(q["question"])

    q.update({
        "bloom_pred": result["bloom_pred"],
        "bloom_conf": result["bloom_conf"],
        "difficulty_pred": result["difficulty_pred"],
        "difficulty_conf": result["difficulty_conf"],
        "bloom_level": result["final_bloom"],
        "difficulty": result["final_difficulty"],
        "bloom_rule": result["bloom_rule"],
        "difficulty_rule": result["difficulty_rule"]
    })

    return q


def clean_question_text(question: str) -> str:
    """
    Cleans generated question text:
    - removes extra spaces
    - ensures it ends with '?'
    """
    question = question.strip()
    question = re.sub(r"\s+", " ", question)

    if not question.endswith("?"):
        question += "?"

    return question



def is_valid_combo(bloom, difficulty):
    return difficulty in BLOOM_DIFFICULTY_MAP.get(bloom, [])
