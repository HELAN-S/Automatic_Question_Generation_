# quality_score.py

def compute_quality_score(question: str):
    score = 0.0

    if not question:
        return 0.0

    words = question.split()
    length = len(words)

    # Length check
    if 6 <= length <= 20:
        score += 0.25

    # Question mark
    if question.strip().endswith("?"):
        score += 0.25

    # Bloom keyword presence
    bloom_words = ["explain", "why", "how", "which", "describe"]

    if any(word in question.lower() for word in bloom_words):
        score += 0.25

    # Avoid vague words
    bad_words = ["widely", "very", "things"]

    if not any(word in question.lower() for word in bad_words):
        score += 0.25

    return round(score, 2)