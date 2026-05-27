# rag/embedder.py

from sentence_transformers import SentenceTransformer
import os

# 🔒 FORCE OFFLINE MODE (CRITICAL)
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"


class Embedder:
    _model = None

    def __init__(self):
        if Embedder._model is None:
            # ✅ LOAD ONCE, REUSE FOREVER
            Embedder._model = SentenceTransformer(
                "all-MiniLM-L6-v2",
                local_files_only=True
            )

        self.model = Embedder._model

    def encode(self, texts):
        return self.model.encode(texts, show_progress_bar=False)
