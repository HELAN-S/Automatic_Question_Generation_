# evaluation/metrics.py
import json
from typing import List, Dict
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
import numpy as np

# -------------------------------
# UTILITY: NORMALIZE LABELS
# -------------------------------
def normalize(labels: List[str]) -> List[str]:
    """
    Lowercase all labels for consistency
    """
    return [str(l).lower() for l in labels]


# -------------------------------
# BLOOM LEVEL EVALUATION
# -------------------------------
def evaluate_bloom_classifier(
    y_true: List[str],
    y_pred: List[str]
) -> Dict:
    """
    Evaluates Bloom Level classifier
    """

    y_true_norm = normalize(y_true)
    y_pred_norm = normalize(y_pred)

    accuracy = accuracy_score(y_true_norm, y_pred_norm)
    macro_f1 = f1_score(y_true_norm, y_pred_norm, average="macro")

    labels = sorted(set(y_true_norm) | set(y_pred_norm))
    conf_matrix = confusion_matrix(y_true_norm, y_pred_norm, labels=labels)

    report = classification_report(
        y_true_norm,
        y_pred_norm,
        labels=labels,
        output_dict=True
    )

    return {
        "accuracy": round(float(accuracy), 4),
        "macro_f1": round(float(macro_f1), 4),
        "confusion_matrix": conf_matrix.tolist(),
        "classification_report": report
    }


# -------------------------------
# DIFFICULTY LEVEL EVALUATION
# -------------------------------
def evaluate_difficulty_classifier(
    y_true: List[str],
    y_pred: List[str]
) -> Dict:
    """
    Evaluates Difficulty classifier (easy / medium / hard)
    """

    y_true_norm = normalize(y_true)
    y_pred_norm = normalize(y_pred)

    accuracy = accuracy_score(y_true_norm, y_pred_norm)
    macro_f1 = f1_score(y_true_norm, y_pred_norm, average="macro")

    # Ensure all labels exist
    labels = sorted(set(y_true_norm) | set(y_pred_norm))
    conf_matrix = confusion_matrix(y_true_norm, y_pred_norm, labels=labels)

    report = classification_report(
        y_true_norm,
        y_pred_norm,
        labels=labels,
        output_dict=True
    )

    return {
        "accuracy": round(float(accuracy), 4),
        "macro_f1": round(float(macro_f1), 4),
        "confusion_matrix": conf_matrix.tolist(),
        "classification_report": report
    }


# -------------------------------
# SYSTEM-LEVEL EVALUATION
# -------------------------------
def system_evaluation(
    questions: List[Dict],
    expected_bloom: List[str],
    expected_difficulty: List[str]
) -> Dict:
    """
    Evaluates entire system output against expected labels
    """

    bloom_preds = [q["bloom_pred"] for q in questions]
    diff_preds = [q["difficulty_pred"] for q in questions]

    bloom_results = evaluate_bloom_classifier(
        expected_bloom,
        bloom_preds
    )

    difficulty_results = evaluate_difficulty_classifier(
        expected_difficulty,
        diff_preds
    )

    return {
        "bloom_evaluation": bloom_results,
        "difficulty_evaluation": difficulty_results,
        "total_questions": len(questions)
    }


# -------------------------------
# SAVE EVALUATION RESULTS
# -------------------------------
def save_evaluation_results(
    results: Dict,
    file_path: str = "evaluation_results.json"
):
    """
    Saves evaluation output to JSON file
    """
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"✅ Evaluation results saved to {file_path}")


# -------------------------------
# SAMPLE TEST RUN (FOR DEBUG)
# -------------------------------
if __name__ == "__main__":

    # SAMPLE GOLD LABELS (ground truth)
   expected_bloom = [
    "Remember",
    "Understand",
    "Remember",
    "Apply",
    "Analyze"
]

    expected_difficulty = [
        "easy",
        "easy",
        "easy",
        "easy",
        "easy"
    ]

    # SAMPLE SYSTEM OUTPUT
    generated_questions = [
        {"bloom_pred": "Knowledge", "difficulty_pred": "easy"},
        {"bloom_pred": "Comprehension", "difficulty_pred": "easy"},
        {"bloom_pred": "Knowledge", "difficulty_pred": "medium"},
        {"bloom_pred": "Application", "difficulty_pred": "easy"},
        {"bloom_pred": "Analysis", "difficulty_pred": "easy"}
    ]

    results = system_evaluation(
        generated_questions,
        expected_bloom,
        expected_difficulty
    )

    save_evaluation_results(results)

    print("\n📊 FINAL EVALUATION SUMMARY")
    print(json.dumps(results, indent=4))
