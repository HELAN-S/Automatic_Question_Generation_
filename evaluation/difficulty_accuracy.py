# evaluation/difficulty_accuracy.py
def difficulty_accuracy(predicted: str, target: str) -> int:
    return int(predicted.lower() == target.lower())
