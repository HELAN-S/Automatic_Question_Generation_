# utils/predictors.py

from transformers import pipeline

# ---------------------------------
# Bloom label mapping
# ---------------------------------
BLOOM_LABEL_MAP = {

    "LABEL_0": "Remember",
    "LABEL_1": "Understand",
    "LABEL_2": "Apply",
    "LABEL_3": "Analyze",
    "LABEL_4": "Evaluate",
    "LABEL_5": "Create",

    "Knowledge": "Remember",
    "Comprehension": "Understand",
    "Application": "Apply",
    "Analysis": "Analyze",
    "Synthesis": "Create",

    None: "Understand"   # 🔥 ADD THIS
}


# ---------------------------------
# Load models
# ---------------------------------

print("Loading Bloom classifier...")

bloom_classifier = pipeline(
    "text-classification",
    model="models/bloom_classifier",
    tokenizer="models/bloom_classifier"
)

print("Loading Difficulty classifier...")

difficulty_classifier = pipeline(
    "text-classification",
    model="models/difficulty_final_model",
    tokenizer="models/difficulty_final_model"
)

print("Models loaded successfully.")


# ---------------------------------
# Bloom prediction (Hybrid)
# ---------------------------------

def predict_bloom(question: str):

    try:

        result = bloom_classifier(question)[0]

        label = result["label"]
        score = result["score"]

        bloom_level = BLOOM_LABEL_MAP.get(label, label)

        q_lower = question.lower()

        # Rule refinement (NOT override always)

        if q_lower.startswith(
            ("what is", "what are", "define", "who is", "when did")
        ):
            bloom_level = "Remember"

        elif q_lower.startswith(
            ("explain", "describe", "summarize")
        ):
            bloom_level = "Understand"

        return bloom_level, score

    except Exception as e:

        print("Bloom prediction failed:", e)

        return "Understand", 0.5


# ---------------------------------
# Difficulty prediction (Hybrid)
# ---------------------------------

def predict_difficulty(question: str):

    try:

        result = difficulty_classifier(question)[0]

        label = result["label"].capitalize()
        score = result["score"]

        word_len = len(question.split())

        # Rule refinement ONLY if mismatch

        if label == "Hard" and word_len < 10:
            label = "Medium"

        if label == "Easy" and word_len > 20:
            label = "Medium"

        return label, score

    except Exception as e:

        print("Difficulty prediction failed:", e)

        return "Medium", 0.5


# ---------------------------------
# Combined prediction
# ---------------------------------

def predict_and_postprocess(question_dict: dict):

    text = question_dict.get("question", "")

    if not text:
        return question_dict

    bloom_label, bloom_conf = predict_bloom(text)
    diff_label, diff_conf = predict_difficulty(text)

    question_dict["bloom_level"] = bloom_label
    question_dict["bloom_confidence"] = round(bloom_conf, 2)

    question_dict["difficulty"] = diff_label
    question_dict["difficulty_confidence"] = round(diff_conf, 2)

    return question_dict