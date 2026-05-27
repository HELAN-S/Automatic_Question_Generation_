# utils/deduplicator.py
import re

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def deduplicate_questions(questions):
    seen = set()
    unique = []

    for q in questions:
        key = normalize(q.get("question", ""))
        if key and key not in seen:
            seen.add(key)
            unique.append(q)

    return unique
