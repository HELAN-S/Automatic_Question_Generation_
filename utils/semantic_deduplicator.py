#semantic_deduplicator.py
from sentence_transformers import SentenceTransformer, util
import os

# -------------------------------
# Load model from local path
# -------------------------------
# Make sure you pre-download the model once and save to this path
MODEL_PATH = "models/all-MiniLM-L6-v2"

if not os.path.exists(MODEL_PATH):
    # First-time download (run manually in Python shell)
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer("all-MiniLM-L6-v2")
    # model.save(MODEL_PATH)
    raise FileNotFoundError(
        f"Model not found at '{MODEL_PATH}'. Please download it first."
    )

model = SentenceTransformer(MODEL_PATH)

# -------------------------------
# Similarity threshold
# -------------------------------
SIM_THRESHOLD = 0.85

# -------------------------------
# Deduplicate questions semantically
# -------------------------------
def semantic_deduplicate(questions):
    """
    Remove questions that are semantically similar based on cosine similarity.
    """
    texts = [q["question"] for q in questions]

    embeddings = model.encode(texts, convert_to_tensor=True)

    unique = []
    used = set()

    for i in range(len(texts)):
        if i in used:
            continue

        unique.append(questions[i])

        for j in range(i + 1, len(texts)):
            if j in used:
                continue

            score = util.cos_sim(embeddings[i], embeddings[j]).item()
            if score > SIM_THRESHOLD:
                used.add(j)

    return unique