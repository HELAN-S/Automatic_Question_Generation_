# evaluation/bloom_accuracy.py
def bloom_accuracy(predicted: str, target: str) -> int:
    return int(predicted.lower() == target.lower())
