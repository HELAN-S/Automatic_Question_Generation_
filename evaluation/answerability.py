# evaluation/answerability.py

def answerability_score(context: str, answer: str) -> float:

    if not context or not answer:
        return 0.0

    if answer.lower() in context.lower():
        return 1.0

    return 0.0