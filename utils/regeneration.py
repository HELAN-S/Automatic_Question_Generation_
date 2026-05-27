# utils/regeneration.py
from typing import Callable, List, Dict, Tuple

def needs_regeneration(target_bloom: str, predicted_bloom: str) -> bool:
    """
    Check if question needs regeneration due to Bloom misalignment
    """
    return target_bloom != predicted_bloom

def auto_regenerate(
    generator_fn: Callable,
    evaluator_fn: Callable,
    filter_fn: Callable,
    enrich_fn: Callable,
    context: str,
    required_count: int,
    eval_args: dict = None,
    max_attempts: int = 3,
    skip_evaluation: bool = False
) -> Tuple[List[Dict], int]:
    """
    Generic auto-regeneration controller
    """
    if eval_args is None:
        eval_args = {}

    all_questions = []
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        needed = required_count - len(all_questions)
        if needed <= 0:
            break

        new_questions = generator_fn(context, needed)
        enriched = [enrich_fn(q) for q in new_questions]

        if not skip_evaluation:
            eval_result = evaluator_fn(
                context=context,
                questions=enriched,
                **eval_args
            )
            for q, r in zip(enriched, eval_result["per_question"]):
                q["quality_score"] = 0.6 * r["relevance"] + 0.4 * int(r["answerable"])

        filtered = filter_fn(enriched)
        all_questions.extend(filtered)

        if len(all_questions) >= required_count:
            break

    return all_questions[:required_count], attempts