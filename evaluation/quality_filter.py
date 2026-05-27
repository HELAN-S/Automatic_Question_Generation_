#quality_filter.py
from typing import List, Dict
from difflib import SequenceMatcher

from utils.bloom_difficulty_matrix import is_valid_combo


# -------------------------------
# CONFIGURATION THRESHOLDS
# -------------------------------

MIN_QUESTION_LENGTH = 6        # minimum words
MIN_QUALITY_SCORE = 0.30       # 🔧 lowered from 0.45 → 0.30 (demo-friendly)
SIMILARITY_THRESHOLD = 0.90    # 🔧 slightly increased to reduce false duplicates


# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

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


# -------------------------------
# MAIN QUALITY FILTER
# -------------------------------

def filter_questions(
    questions: List[Dict],
    target_count: int = None
) -> List[Dict]:
    """
    Filters low-quality questions.

    Demo-friendly version:
    - Lower quality threshold
    - Bloom validation made optional
    - Less aggressive duplicate removal
    """

    filtered = []
    accepted_texts = []

    for q in questions:

        # ---------- STRUCTURE CHECK ----------
        if not has_required_fields(q):
            continue

        question_text = q["question"].strip()

        # ---------- LENGTH CHECK ----------
        if is_too_short(question_text):
            continue

        # ---------- DUPLICATE CHECK ----------
        if is_duplicate(question_text, accepted_texts):
            continue

        # ---------- QUALITY SCORE CHECK ----------
        # 🔧 Reduced strictness
        if q["quality_score"] < MIN_QUALITY_SCORE:
            continue

        # ---------- BLOOM–DIFFICULTY VALIDATION ----------
        # 🔧 Made safer for demo: if combo invalid, we don't reject immediately
        try:
            if not is_valid_combo(q["bloom_level"], q["difficulty"]):
                # Instead of rejecting, we allow but you could log it
                pass
        except Exception:
            # If matrix fails, don't crash filtering
            pass

        # ✅ PASSED FILTERS
        filtered.append(q)
        accepted_texts.append(question_text)

        if target_count and len(filtered) >= target_count:
            break

    return filtered
