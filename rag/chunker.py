#rag/chunker.py
from typing import List
import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize


def chunk_text(text: str, max_words: int = 400) -> List[str]:
    """
    Converts text into semantic chunks.
    """
    sentences = sent_tokenize(text)
    chunks = []

    current_chunk = []
    word_count = 0

    for sent in sentences:
        words = sent.split()
        if word_count + len(words) > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0

        current_chunk.append(sent)
        word_count += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
