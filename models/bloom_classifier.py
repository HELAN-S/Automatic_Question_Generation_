# models/bloom_classifier.py
import os
import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class BloomClassifier:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, "models", "bloom_model")

        # 🔹 Temporary debug prints
        print("Loading Bloom model from:", model_path)

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("Tokenizer loaded successfully ✅")

        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        print("Model loaded successfully ✅")

        # Print number of parameters as a sanity check
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"Total parameters in Bloom model: {total_params}")

        # Forward pass test
        try:
            dummy_input = self.tokenizer("Define photosynthesis", return_tensors="pt")
            with torch.no_grad():
                dummy_logits = self.model(**dummy_input).logits
            print("Forward pass successful. Sample logits:", dummy_logits)
        except Exception as e:
            print("Forward pass failed:", e)

        self.labels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

        # ✅ Strong verb-based override mapping
        self.verb_map = {
            "define": "Remember",
            "list": "Remember",
            "identify": "Remember",
            "state": "Remember",

            "explain": "Understand",
            "describe": "Understand",
            "summarize": "Understand",

            "apply": "Apply",
            "solve": "Apply",
            "use": "Apply",

            "compare": "Analyze",
            "differentiate": "Analyze",
            "analyze": "Analyze",

            "evaluate": "Evaluate",
            "justify": "Evaluate",
            "criticize": "Evaluate",

            "design": "Create",
            "create": "Create",
            "develop": "Create",
            "construct": "Create"
        }

    def rule_based_prediction(self, text: str):
        text = text.lower()
        for verb, level in self.verb_map.items():
            if re.search(rf"\b{verb}\b", text):
                return level
        return None

    def model_prediction(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        return self.labels[torch.argmax(logits).item()]

    def predict(self, text: str) -> str:
        # 🔥 Priority 1: Rule-based verb mapping
        rule_label = self.rule_based_prediction(text)
        if rule_label:
            return rule_label

        # 🔥 Priority 2: ML model fallback
        return self.model_prediction(text)


# 🔹 Instantiate a global classifier
_classifier = BloomClassifier()


def predict_bloom(text: str) -> str:
    return _classifier.predict(text)