#utils/bloom_normalizer.py
def normalize_bloom(bloom: str) -> str:
    if not bloom:
        return "understand"

    bloom = bloom.strip().lower()

    mapping = {
        "knowledge": "remember",
        "remembering": "remember",

        "comprehension": "understand",
        "understanding": "understand",

        "application": "apply",
        "applying": "apply",

        "analysis": "analyze",
        "analyzing": "analyze",

        "evaluation": "evaluate",
        "evaluating": "evaluate",

        "creation": "create",
        "creating": "create"
    }

    return mapping.get(bloom, bloom)
