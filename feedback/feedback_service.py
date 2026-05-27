# feedback/feedback_service.py
from database.db import get_db
from typing import Optional, Dict, List


def submit_feedback(
    question_id: int,
    usefulness: int,
    relevance: int,
    comments: Optional[str] = None
) -> bool:
    """
    Stores user feedback for a generated question
    """

    # Safety check if somehow non-integer is passed
    try:
        usefulness = int(usefulness)
        relevance = int(relevance)
    except ValueError:
        raise ValueError("Usefulness and relevance must be integers between 1 and 5")

    if usefulness < 1 or usefulness > 5:
        raise ValueError("Usefulness must be between 1 and 5")
    if relevance < 1 or relevance > 5:
        raise ValueError("Relevance must be between 1 and 5")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO feedback
        (question_id, usefulness, relevance, comments)
        VALUES (%s, %s, %s, %s)
    """, (
        question_id,
        usefulness,
        relevance,
        comments
    ))

    db.commit()
    cursor.close()
    db.close()

    return True


def get_feedback_by_question(question_id: int) -> List[Dict]:
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT usefulness, relevance, comments, submitted_at
        FROM feedback
        WHERE question_id = %s
    """, (question_id,))

    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def get_feedback_summary(question_id: int) -> Dict:
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            AVG(usefulness) AS avg_usefulness,
            AVG(relevance) AS avg_relevance,
            COUNT(*) AS total_feedback
        FROM feedback
        WHERE question_id = %s
    """, (question_id,))

    result = cursor.fetchone()
    cursor.close()
    db.close()

    return {
        "question_id": question_id,
        "avg_usefulness": round(result["avg_usefulness"], 2) if result["avg_usefulness"] else 0.0,
        "avg_relevance": round(result["avg_relevance"], 2) if result["avg_relevance"] else 0.0,
        "total_feedback": result["total_feedback"]
    }


def is_question_low_quality(question_id: int, threshold: float = 2.5) -> bool:
    summary = get_feedback_summary(question_id)
    if summary["total_feedback"] == 0:
        return False  # no feedback yet
    avg_score = (summary["avg_usefulness"] + summary["avg_relevance"]) / 2
    return avg_score < threshold