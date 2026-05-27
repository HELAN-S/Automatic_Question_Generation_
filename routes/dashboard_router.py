from fastapi import APIRouter, Depends
from database.db import get_db
from collections import Counter

from auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# -----------------------------
# Normalize Bloom Labels
# -----------------------------
def normalize_bloom(label):

    if not label:
        return "Understand"

    mapping = {
        "Analysis": "Analyze",
        "Comprehension": "Understand",
        "Application": "Apply",
        "Synthesis": "Create",
    }

    return mapping.get(label, label)


# -----------------------------
# Dashboard Stats API
# -----------------------------
@router.get("/stats")
def get_dashboard_stats(
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    conn = get_db()
    cur = conn.cursor()

    # -------------------------
    # Total Questions
    # -------------------------
    cur.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE user_id=%s
    """, (user_id,))

    total_questions = cur.fetchone()[0]

    # -------------------------
    # Distribution Query
    # -------------------------
    cur.execute("""
        SELECT
            bloom_level,
            difficulty,
            question_type
        FROM questions
        WHERE user_id=%s
    """, (user_id,))

    bloom_counter = Counter()
    diff_counter = Counter()
    type_counter = Counter()

    for bloom, difficulty, qtype in cur.fetchall():

        bloom_counter[normalize_bloom(bloom)] += 1
        diff_counter[difficulty or "Medium"] += 1
        type_counter[qtype or "short"] += 1

    # -------------------------
    # Recent Questions
    # -------------------------
    cur.execute("""
        SELECT
            question_text,
            question_type,
            bloom_level,
            difficulty
        FROM questions
        WHERE user_id=%s
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))

    recent_questions = [

        {
            "question": row[0],
            "type": row[1],
            "bloom_level": normalize_bloom(row[2]),
            "difficulty": row[3],
        }

        for row in cur.fetchall()
    ]

    # -------------------------
    # PDF Stats
    # -------------------------
    cur.execute("""
        SELECT COUNT(*)
        FROM documents
        WHERE user_id=%s
    """, (user_id,))

    total_pdfs = cur.fetchone()[0]

    cur.execute("""
        SELECT SUM(num_chunks)
        FROM documents
        WHERE user_id=%s
    """, (user_id,))

    result = cur.fetchone()

    total_chunks = result[0] if result and result[0] else 0

    # -------------------------
    # Average Quality
    # -------------------------
    cur.execute("""
        SELECT AVG(quality_score)
        FROM questions
        WHERE user_id=%s
    """, (user_id,))

    result = cur.fetchone()

    avg_quality = result[0] if result and result[0] else 0

    conn.close()

    return {

        "total_questions": total_questions,

        "total_pdfs": total_pdfs,

        "total_pdf_chunks": total_chunks,

        "bloom_distribution": dict(bloom_counter),

        "difficulty_distribution": dict(diff_counter),

        "type_distribution": dict(type_counter),

        "recent_questions": recent_questions,

        "average_quality_score": round(avg_quality, 2)

    }