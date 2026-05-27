# utils/postprocess.py

import re


# -------------------------------
# Main Cleaner
# -------------------------------

def clean_question_text(
    question: str
):

    if not question:
        return ""

    question = question.strip()

    # -------------------------------
    # Normalize spaces
    # -------------------------------

    question = re.sub(
        r"\s+",
        " ",
        question
    )

    # -------------------------------
    # Fix blank spacing
    # -------------------------------

    question = re.sub(
        r"_+\s*",
        "_____ ",
        question
    )

    question = re.sub(
        r"\s+_____",
        " _____",
        question
    )

    # -------------------------------
    # Remove duplicate punctuation
    # -------------------------------

    question = re.sub(
        r"\?+",
        "?",
        question
    )

    question = re.sub(
        r"\s+\?",
        "?",
        question
    )

    # -------------------------------
    # Grammar Fix Patterns
    # -------------------------------

    fixes = {

        "Explain about": "Explain",

        "Explain the concept of": "Explain",

        "What is significant challenges":
            "What are significant challenges",

        "What is the types of":
            "What are the types of",

        "How does works":
            "How does it work",

        "What is used to":
            "What is used to"

    }

    for wrong, correct in fixes.items():

        question = question.replace(
            wrong,
            correct
        )

    # -------------------------------
    # Remove duplicate words
    # -------------------------------

    question = re.sub(
        r"\b(\w+)\s+\1\b",
        r"\1",
        question,
        flags=re.IGNORECASE
    )

    # -------------------------------
    # Capitalize First Letter
    # -------------------------------

    if question:

        question = (

            question[0].upper()

            + question[1:]

        )

    # -------------------------------
    # Ensure Question Mark
    # -------------------------------

    if not question.endswith("?"):

        question += "?"

    return question