# generators/generation_service.py

import random

from generators.mcq_generator import generate_mcq
from generators.fib_generator import generate_fib
from generators.true_false_generator import generate_true_false
from generators.short_answer_generator import generate_short_questions

from utils.postprocess import clean_question_text
from utils.predictors import predict_and_postprocess

random.seed(42)


# -------------------------------
# TYPE MAP
# -------------------------------

TYPE_MAP = {
    "mcq": "mcq",
    "multiple_choice": "mcq",
    "true_false": "true_false",
    "fib": "fib",
    "fill_in_the_blanks": "fib",
    "short_answer": "short"
}


def map_to_enum_type(q_type):

    if not q_type:
        return "short"

    return TYPE_MAP.get(
        q_type.lower().strip(),
        "short"
    )


# -------------------------------
# VALIDATION
# -------------------------------

def is_valid(q):

    text = q.get("question", "").lower()

    if not text:
        return False

    words = text.split()

    if len(words) < 3 or len(words) > 30:
        return False

    bad_phrases = [
        "in an era",
        "at its core",
        "as businesses"
    ]

    if any(p in text for p in bad_phrases):
        return False

    return True


# -------------------------------
# DEDUPLICATION
# -------------------------------

def deduplicate(questions):

    seen = set()
    final = []

    for q in questions:

        key = q["question"].strip().lower()[:80]

        if key in seen:
            continue

        seen.add(key)
        final.append(q)

    return final


# -------------------------------
# MAIN FUNCTION
# -------------------------------

def generate_question_paper(
    context=None,
    source=None,
    total_questions=5,
    question_types=None,
    target_bloom_levels=None,
    target_difficulty_levels=None,
    bloom_distribution=None,
    **kwargs
):

    if not context:
        context = ""

    if not question_types:
        question_types = ["short_answer"]

    question_types = [
        q.lower().strip()
        for q in question_types
    ]

    generators = {
        "mcq": generate_mcq,
        "fib": generate_fib,
        "true_false": generate_true_false,
        "short_answer": generate_short_questions
    }

    # -------------------------------
    # STEP 1 — GENERATE POOL
    # -------------------------------

    pool = []

    per_type_count = max(
        1,
        total_questions // len(question_types)
    )

    for qtype in question_types:

        gen_fn = generators.get(qtype)

        if not gen_fn:
            continue

        try:

            qs = gen_fn(
                context,
                per_type_count * 5,
                target_bloom_levels,
                target_difficulty_levels,
                bloom_distribution
            )

            for q in qs:
                q["type"] = qtype

            pool.extend(qs)

        except Exception as e:

            print(
                "Generator error:",
                qtype,
                e
            )

    # -------------------------------
    # STEP 2 — CLEAN
    # -------------------------------

    cleaned = []

    for q in pool:

        q["question"] = clean_question_text(
            q.get("question", "")
        )

        if not is_valid(q):
            continue

        cleaned.append(q)

    cleaned = deduplicate(cleaned)

    if not cleaned:
        return {
            "source": source,
            "total_questions": 0,
            "questions": []
        }

    # -------------------------------
    # STEP 3 — Bloom Plan
    # -------------------------------

    bloom_plan = []

    if bloom_distribution:

        for k, v in bloom_distribution.items():
            bloom_plan += [k] * v

    while len(bloom_plan) < total_questions:

        bloom_plan.append(
            random.choice(
                target_bloom_levels
                or ["Understand"]
            )
        )

    # -------------------------------
    # STEP 4 — FINAL OUTPUT
    # -------------------------------

    final_output = []

    for i, q in enumerate(cleaned):

        if len(final_output) >= total_questions:
            break

        # ML Prediction
        q = predict_and_postprocess(q)

        # FIXED LOGIC (IMPORTANT)

        # Only adjust if mismatch

        if (
            target_bloom_levels
            and q["bloom_level"]
            not in target_bloom_levels
        ):
            q["bloom_level"] = bloom_plan[i]

        if (
            target_difficulty_levels
            and q["difficulty"]
            not in target_difficulty_levels
        ):
            q["difficulty"] = random.choice(
                target_difficulty_levels
            )

        q["type"] = map_to_enum_type(
            q.get("type")
        )

        final_output.append(q)

    return {
        "source": source,
        "total_questions": len(final_output),
        "questions": final_output
    }