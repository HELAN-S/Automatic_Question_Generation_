# utils/quality_control.py

MIN_BLOOM_CONFIDENCE = 0.55
MIN_DIFFICULTY_CONFIDENCE = 0.60


def is_low_quality(question: dict) -> bool:
    text = question.get("question", "").lower()
    options = question.get("options", [])

    if len(options) != 4:
        return True

    if len(set(options)) < 4:
        return True

    if any(len(o.split()) < 2 for o in options):
        return True

    if len(text.split()) < 5:
        return True

    return False

def is_valid_short_question(q: str) -> bool:
    if len(q.split()) < 6:
        return False
    if len(q) > 200:
        return False
    if any(x in q.lower() for x in ["%", "=", "{", "}", "_", "\\"]):
        return False
    return True
