from fastapi import APIRouter, UploadFile, File, Depends
from database.db import get_db
import uuid
from rag.pdf_loader import load_pdf_text
from rag.chunker import chunk_text
from rag.embedder import Embedder
from rag.state import vector_store
from auth.jwt_handler import get_current_user  # inject logged-in user

router = APIRouter()

@router.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)  # ✅ logged-in user
):

    conn = get_db()
    cur = conn.cursor()

    # Extract text
    text = await load_pdf_text(file)
    if not text:
        return {"error": "PDF text extraction failed"}

    # Chunk text
    chunks = chunk_text(text)

    # Generate embeddings
    embedder = Embedder()
    embeddings = embedder.encode(chunks)

    # Document ID
    document_id = int(uuid.uuid4().int % 100000)

    # Store in FAISS
    vector_store.add(
        embeddings=embeddings,
        texts=chunks,
        document_id=document_id
    )

    # Store in DB
    filename = file.filename
    num_chunks = len(chunks)
    user_id = current_user["id"]  # ✅ use actual user

    cur.execute(
        """
        INSERT INTO documents (filename, num_chunks, user_id)
        VALUES (%s, %s, %s)
        """,
        (filename, num_chunks, user_id)
    )

    conn.commit()
    conn.close()

    return {
        "message": "PDF uploaded & indexed successfully",
        "document_id": document_id,
        "filename": filename,
        "chunks": num_chunks
    }