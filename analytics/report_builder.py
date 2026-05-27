#analytics/report_builder.py
from analytics.aggregator import aggregate_questions
from evaluation.evaluator import evaluate_questions


def build_analytics_report(
    context: str,
    questions: list,
    evaluation_results: dict,
    regeneration_attempts: dict
):
    """
    Build a final analytics report for UI / export
    """

    aggregation = aggregate_questions(questions)

    return {
        "summary": aggregation,
        "evaluation": evaluation_results,
        "regeneration": regeneration_attempts,
        "context_length": len(context.split())
    }
