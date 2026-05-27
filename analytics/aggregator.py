# analytics/aggregator.py

from collections import Counter

from evaluation.relevance import relevance_score
from evaluation.diversity import diversity_score
from evaluation.answerability import answerability_score
from utils.quality_score import compute_quality_score


def aggregate_questions(data):

    questions = data.get("questions", [])
    context = data.get("context", "")

    if not questions:
        return default_response()

    # -----------------------------
    # DISTRIBUTIONS
    # -----------------------------

    bloom_counter = Counter()
    difficulty_counter = Counter()
    type_counter = Counter()

    relevance_list = []
    answerability_list = []
    quality_list = []

    for q in questions:

        bloom = q.get("bloom_level", "Unknown")
        difficulty = q.get("difficulty", "Unknown")
        qtype = q.get("type", "Unknown")

        bloom_counter[bloom] += 1
        difficulty_counter[difficulty] += 1
        type_counter[qtype] += 1

        # -------------------------
        # QUALITY PER QUESTION
        # -------------------------

        q_text = q.get("question", "")

        q_score = compute_quality_score(q_text)

        quality_list.append(q_score)

        # -------------------------
        # RELEVANCE
        # -------------------------

        if context:

            rel = relevance_score(
                context,
                q_text
            )

            relevance_list.append(rel)

        # -------------------------
        # ANSWERABILITY
        # -------------------------

        ans = q.get("answer")

        if context and ans:

            ans_score = answerability_score(
                context,
                ans
            )

            answerability_list.append(ans_score)

    # -----------------------------
    # AVERAGES
    # -----------------------------

    avg_quality = (
        sum(quality_list) / len(quality_list)
        if quality_list else 0
    )

    avg_relevance = (
        sum(relevance_list) / len(relevance_list)
        if relevance_list else 0
    )

    avg_answerability = (
        sum(answerability_list) / len(answerability_list)
        if answerability_list else 0
    )

    diversity = diversity_score(questions)

    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_score = round(

        (
            avg_quality * 0.4 +
            avg_relevance * 0.2 +
            avg_answerability * 0.2 +
            diversity * 0.2
        ),

        2
    )

    return {

        "total_questions": len(questions),

        "bloom_distribution":
            dict(bloom_counter),

        "difficulty_distribution":
            dict(difficulty_counter),

        "question_type_distribution":
            dict(type_counter),

        "avg_relevance":
            round(avg_relevance, 2),

        "avg_answerability":
            round(avg_answerability, 2),

        "diversity_score":
            diversity,

        "final_quality_score":
            final_score
    }


def default_response():

    return {

        "total_questions": 0,

        "bloom_distribution": {},

        "difficulty_distribution": {},

        "question_type_distribution": {},

        "avg_relevance": 0,

        "avg_answerability": 0,

        "diversity_score": 0,

        "final_quality_score": 0
    }