# evaluation/diversity.py

def diversity_score(questions: list) -> float:

    texts = [
        q.get("question", "").lower().strip()
        for q in questions
        if q.get("question")
    ]

    if not texts:
        return 0.0

    unique = len(set(texts))

    return round(unique / len(texts), 2)