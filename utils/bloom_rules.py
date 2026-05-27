#utils/bloom_rules.py
# Strict Bloom verbs for controlled question generation
BLOOM_VERB_MAP = {
    "Remember": ["Define", "List", "Identify"],
    "Understand": ["Explain", "Summarize", "Describe"],
    "Apply": ["Apply", "Demonstrate", "Use"],
    "Analyze": ["Analyze", "Compare", "Differentiate"],
    "Evaluate": ["Evaluate", "Justify", "Critique"],
    "Create": ["Design", "Develop", "Construct"]
}

# Mapping model output labels to standard Bloom levels
BLOOM_MAP = {
    "LABEL_0": "Remember",
    "LABEL_1": "Understand",
    "LABEL_2": "Apply",
    "LABEL_3": "Analyze",
    "LABEL_4": "Evaluate",
    "LABEL_5": "Create"
}

def map_bloom(label: str) -> str:
    """
    Convert model label to standard Bloom level
    """
    return BLOOM_MAP.get(label, "Understand")

# -----------------------
# Post-generation Bloom validation rules
# -----------------------

def apply_bloom_rules(question: str, model_bloom: str, confidence: float):
    """
    Simple rules to validate or adjust Bloom level for a generated question
    Returns (final_bloom, applied_rule)
    """
    q = question.lower().strip()

    LOW_LEVEL_VERBS = ["define", "state", "list", "identify", "name", "what is"]
    COMPREHENSION_VERBS = ["explain", "describe", "summarize", "illustrate"]
    APPLICATION_VERBS = ["apply", "use", "demonstrate", "solve", "implement"]
    ANALYSIS_VERBS = ["analyze", "compare", "differentiate", "why", "how"]

    # Rule 1: Verb-based
    if any(v in q for v in ANALYSIS_VERBS):
        return "Analyze", "verb_rule"
    if any(v in q for v in APPLICATION_VERBS):
        return "Apply", "verb_rule"
    if any(v in q for v in COMPREHENSION_VERBS):
        return "Understand", "verb_rule"
    if any(v in q for v in LOW_LEVEL_VERBS):
        return "Remember", "verb_rule"

    # Rule 2: Low confidence fallback
    if confidence < 0.75:
        return "Remember", "low_confidence_rule"

    # Rule 3: Statement fallback (no question mark)
    if not q.endswith("?"):
        return "Remember", "statement_rule"

    # Rule 4: Default – trust model
    return model_bloom, "model"