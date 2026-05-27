# utils/difficulty_rules.py
def apply_difficulty_rules(bloom_level: str):

    bloom_level = bloom_level.capitalize()

    if bloom_level in ["Remember", "Understand"]:
        return "Easy"

    if bloom_level in ["Apply", "Analyze"]:
        return "Medium"

    if bloom_level in ["Evaluate", "Create"]:
        return "Hard"

    return "Medium"