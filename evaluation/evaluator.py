# evaluation/evaluator.py

from typing import List, Dict


def evaluate_questions(
    questions: List[Dict],
    context: str = None
) -> Dict:

    if not questions:
        return {
            "diversity_score": 0,
            "avg_relevance": 0,
            "avg_answerability": 0,
            "heuristic_quality": 0,
            "final_quality_score": 0
        }

    # ---------------------------------
    # DIVERSITY
    # ---------------------------------

    question_texts = [
        q.get("question", "").lower().strip()
        for q in questions
    ]

    unique_questions = len(set(question_texts))

    diversity_score = (
        unique_questions /
        len(question_texts)
    )

    # ---------------------------------
    # RELEVANCE
    # ---------------------------------

    relevance_scores = []

    if context:

        context_words = set(
            context.lower().split()
        )

        for q in questions:

            question_words = set(
                q.get("question", "")
                .lower()
                .split()
            )

            if not question_words:
                relevance_scores.append(0)
                continue

            match = len(
                context_words.intersection(
                    question_words
                )
            )

            # ✅ Correct formula

            score = match / len(question_words)

            relevance_scores.append(score)

    else:

        relevance_scores = [0.5] * len(questions)

    avg_relevance = (
        sum(relevance_scores) /
        len(relevance_scores)
    )

    # ---------------------------------
    # ANSWERABILITY
    # ---------------------------------

    answerability_scores = []

    if context:

        context_words = set(
            context.lower().split()
        )

        for q in questions:

            answer = q.get("answer", "")

            answer_words = set(
                answer.lower().split()
            )

            if not answer_words:

                answerability_scores.append(0)

                continue

            match = len(
                context_words.intersection(
                    answer_words
                )
            )

            score = match / len(answer_words)

            answerability_scores.append(score)

    else:

        answerability_scores = [0.5] * len(questions)

    avg_answerability = (
        sum(answerability_scores) /
        len(answerability_scores)
    )

    # ---------------------------------
    # FINAL QUALITY
    # ---------------------------------

    heuristic_quality = (

        avg_relevance * 0.4 +

        avg_answerability * 0.4 +

        diversity_score * 0.2
    )

    final_quality_score = round(
        heuristic_quality,
        2
    )

    return {

        "diversity_score":
            round(diversity_score, 2),

        "avg_relevance":
            round(avg_relevance, 2),

        "avg_answerability":
            round(avg_answerability, 2),

        "heuristic_quality":
            round(heuristic_quality, 2),

        "final_quality_score":
            final_quality_score
    }