# evaluation/relevance.py

def relevance_score(context: str, question: str) -> float:

    if not context or not question:
        return 0.0

    ctx_words = set(context.lower().split())
    q_words = set(question.lower().split())

    if not q_words:
        return 0.0

    overlap = ctx_words.intersection(q_words)

    score = len(overlap) / len(q_words)

    return round(score, 2)