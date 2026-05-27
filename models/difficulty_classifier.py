# models/difficulty_classifier.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class DifficultyClassifier:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, "models", "difficulty_final_model")

        # 🔹 Temporary debug prints
        print("Loading Difficulty model from:", model_path)

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("Tokenizer loaded successfully ✅")

        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        print("Model loaded successfully ✅")

        # Print number of parameters as a sanity check
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"Total parameters in Difficulty model: {total_params}")

        # Forward pass test
        try:
            dummy_input = self.tokenizer("Solve this equation", return_tensors="pt")
            with torch.no_grad():
                dummy_logits = self.model(**dummy_input).logits
            print("Forward pass successful. Sample logits:", dummy_logits)
        except Exception as e:
            print("Forward pass failed:", e)

        self.labels = ["Easy", "Medium", "Hard"]

    def predict(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        return self.labels[torch.argmax(logits).item()]


# 🔹 Instantiate a global classifier
_difficulty_classifier = DifficultyClassifier()


def predict_difficulty(text: str) -> str:
    return _difficulty_classifier.predict(text)