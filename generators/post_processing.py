#generators\post_processing.py
import re

def clean_question(question: str) -> str:
    question = question.strip()

    # Remove incomplete fragments
    if len(question.split()) < 6:
        return None

    # Fix grammar patterns
    question = re.sub(r"\bHow is\b", "How is the", question)
    question = re.sub(r"\bExplain tasks such\b", "Explain the tasks such as", question)

    # Ensure question mark
    if not question.endswith("?"):
        question += "?"

    return question