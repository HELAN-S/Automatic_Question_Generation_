# utils/model_loader.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---------- Difficulty model ----------
DIFF_MODEL_PATH = "./models/difficulty_final_model"  # <- Corrected path
if not os.path.exists(DIFF_MODEL_PATH):
    raise FileNotFoundError(f"Difficulty model folder not found at {DIFF_MODEL_PATH}")

diff_tokenizer = AutoTokenizer.from_pretrained(DIFF_MODEL_PATH, local_files_only=True)
diff_model = AutoModelForSequenceClassification.from_pretrained(
    DIFF_MODEL_PATH, local_files_only=True
).to(DEVICE)
diff_model.eval()

# ---------- BLOOM model ----------
BLOOM_MODEL_PATH = "./models/bloom_model"  # <- Corrected path
if not os.path.exists(BLOOM_MODEL_PATH):
    raise FileNotFoundError(f"BLOOM model folder not found at {BLOOM_MODEL_PATH}")

bloom_tokenizer = AutoTokenizer.from_pretrained(BLOOM_MODEL_PATH, local_files_only=True)
bloom_model = AutoModelForSequenceClassification.from_pretrained(
    BLOOM_MODEL_PATH, local_files_only=True
).to(DEVICE)
bloom_model.eval()