#backend/balancer.py
from collections import defaultdict
import math

DEFAULT_BLOOM_RATIO = {
    "Knowledge": 0.2,
    "Comprehension": 0.25,
    "Application": 0.2,
    "Analysis": 0.15,
    "Evaluation": 0.1,
    "Synthesis": 0.1,
    "Needs Review": 0.1
}


DEFAULT_DIFFICULTY_RATIO = {
    "easy": 0.4,
    "medium": 0.4,
    "hard": 0.2
}


def mark_low_confidence(q, threshold=0.6):
    if q["bloom_confidence"] < threshold:
        q["bloom_level"] = "Needs Review"
    return q


def balance_by_ratio(items, key, ratio_map, total):
    grouped = defaultdict(list)

    for item in items:
        grouped[item[key]].append(item)

    balanced = []
    for label, ratio in ratio_map.items():
        take = math.ceil(ratio * total)
        balanced.extend(grouped.get(label, [])[:take])

    return balanced



def rebalance_questions(questions, target_difficulty, num_questions):
    """
    Select questions matching target difficulty.
    Falls back gracefully if not enough.
    """
    buckets = defaultdict(list)

    for q in questions:
        buckets[q["difficulty"]].append(q)

    selected = []

    for diff in target_difficulty:
        selected.extend(buckets.get(diff, []))

    # fallback if insufficient
    if len(selected) < num_questions:
        for diff, qs in buckets.items():
            if diff not in target_difficulty:
                selected.extend(qs)

    return selected[:num_questions]
