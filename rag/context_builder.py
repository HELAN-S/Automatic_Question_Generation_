# rag/context_builder.py
from fastapi import UploadFile
from typing import List
from rag.pdf_loader import load_pdf_text
from rag.retriever import retrieve_chunks

async def load_pdf(upload_file: UploadFile) -> str:
    contents = await upload_file.read()
    text = load_pdf_text(contents)
    return text

def build_augmented_context(user_context: str, retrieved_chunks: List[str]) -> str:
    if not retrieved_chunks:
        return user_context
    # Limit top 3 chunks ✅
    top_chunks = retrieved_chunks[:3]
    return user_context + "\n\n--- Retrieved Knowledge ---\n" + "\n\n".join(top_chunks)

def build_context_from_chunks(chunks: List[str]) -> str:
    if not chunks:
        return ""
    # Limit top 3 chunks ✅
    return "\n\n".join(chunks[:3])

async def build_context(source_type: str, text: str = None, upload_file: UploadFile = None) -> str:
    chunks = []

    if source_type.lower() == "pdf" and upload_file is not None:
        pdf_text = await load_pdf(upload_file)
        if pdf_text:
            chunks.append(pdf_text)
    elif source_type.lower() == "text" and text:
        chunks.append(text)

    retrieved = retrieve_chunks(chunks)
    context = build_augmented_context(" ".join(chunks), retrieved)
    return context