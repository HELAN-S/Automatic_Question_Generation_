# jobs/generate_worker.py
from generators.generation_service import generate_question_paper
from rag.retriever import retrieve_relevant_chunks
from jobs.job_store import JOB_STORE

# ⭐ ADD THESE
from database.logger import log_question, log_prediction


def run_generation(job_id: str, payload: dict):
    try:

        JOB_STORE.set_running(job_id)

        context = ""

        # -------------------------------
        # ⭐ GET USER ID
        # -------------------------------

        user_id = payload.get("user_id")

        print("USER ID:", user_id)

        # -------------------------------
        # BUILD CONTEXT
        # -------------------------------

        source_type = payload.get("source_type", "").lower()

        if source_type == "text":

            context = payload.get("text", "")

        elif source_type == "pdf":

            document_id = payload.get("document_id")

            if not document_id:
                raise ValueError(
                    "document_id required for PDF mode"
                )

            retrieved_chunks = retrieve_relevant_chunks(
                int(document_id),
                "generate questions",
                top_k=5
            )

            if not retrieved_chunks:
                raise ValueError(
                    "No chunks found for this document"
                )

            context = "\n\n".join(retrieved_chunks)

        else:

            raise ValueError(
                f"Unsupported source_type: {source_type}"
            )

        if not context.strip():
            raise ValueError("Context is empty")

        print("📄 Context Length:", len(context))

        # -------------------------------
        # GENERATE QUESTIONS
        # -------------------------------

        result = generate_question_paper(
            context=context,
            source=payload.get("source_type"),
            total_questions=payload.get("num_questions", 5),
            question_types=payload.get("question_types"),
            target_bloom_levels=payload.get("target_bloom_levels"),
            target_difficulty_levels=payload.get("target_difficulty_levels"),
            bloom_distribution=payload.get("bloom_distribution")
        )

        questions = result.get("questions", [])

        print("TOTAL GENERATED:", len(questions))

        # -------------------------------
        # ⭐ SAVE QUESTIONS TO DB
        # -------------------------------

        for q in questions:

            print("Saving question:", q.get("question"))

            q_id = log_question(
                q,
                user_id,
                context
            )

            log_prediction(
                q_id,
                q
            )

        # -------------------------------
        # COMPLETE JOB
        # -------------------------------

        JOB_STORE.complete_job(
            job_id,
            result
        )

    except Exception as e:

        print("❌ GENERATION FAILED:", str(e))

        JOB_STORE.fail_job(
            job_id,
            f"Generation failed: {str(e)}"
        )