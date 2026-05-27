# utils/quality_filter.py
from typing import List, Dict
from difflib import SequenceMatcher

MIN_QUESTION_LENGTH = 5
MIN_QUALITY_SCORE = 0.5  # strict
SIMILARITY_THRESHOLD = 0.9

def is_too_short(question: str) -> bool:
    return len(question.split()) < MIN_QUESTION_LENGTH

def similarity(q1: str, q2: str) -> float:
    return SequenceMatcher(None, q1.lower(), q2.lower()).ratio()

def is_duplicate(question: str, accepted: List[str]) -> bool:
    for q in accepted:
        if similarity(question, q) > SIMILARITY_THRESHOLD:
            return True
    return False

def has_required_fields(q: Dict) -> bool:
    required = ["question", "difficulty", "bloom_level", "quality_score"]
    return all(field in q for field in required)

def reject_low_quality(question: Dict) -> bool:
    if len(question.get("question","").split()) < 5:
        return True
    if question.get("quality_score", 0) < MIN_QUALITY_SCORE:
        return True
    return False

def remove_similar_questions(questions: List[Dict]) -> List[Dict]:
    unique = []
    texts = set()
    for q in questions:
        if q["question"] not in texts:
            texts.add(q["question"])
            unique.append(q)
    return unique

def filter_questions(questions: List[Dict], target_count: int = None) -> List[Dict]:
    filtered = []
    accepted_texts = []

    for q in questions:
        if not has_required_fields(q) or reject_low_quality(q):
            continue
        if is_duplicate(q["question"], accepted_texts):
            continue
        filtered.append(q)
        accepted_texts.append(q["question"])
        if target_count and len(filtered) >= target_count:
            break

    # Ensure diversity ✅
    filtered = remove_similar_questions(filtered)
    return filtered
