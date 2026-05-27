# database/logger.py
from database.db import get_db


def log_question(q, user_id, context=""):

    try:

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO questions
            (
                user_id,
                question_text,
                answer_text,
                question_type,
                bloom_level,
                difficulty,
                quality_score,
                source_context
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (

            user_id,

            q.get("question"),
            q.get("answer"),
            q.get("type"),
            q.get("bloom_level"),
            q.get("difficulty"),
            q.get("quality_score", 0),

            context

        ))

        db.commit()

        q_id = cursor.lastrowid

        return q_id

    except Exception as e:

        print("LOG_QUESTION ERROR:", e)
        raise e

    finally:

        cursor.close()
        db.close()


def log_prediction(q_id, q):

    try:

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO predictions
            (
                question_id,
                bloom_pred,
                bloom_conf,
                difficulty_pred,
                difficulty_conf
            )
            VALUES (%s,%s,%s,%s,%s)
        """, (

            q_id,
            q.get("bloom_level"),
            q.get("bloom_confidence"),
            q.get("difficulty"),
            q.get("difficulty_confidence")

        ))

        db.commit()

    except Exception as e:

        print("LOG_PREDICTION ERROR:", e)
        raise e

    finally:

        cursor.close()
        db.close()