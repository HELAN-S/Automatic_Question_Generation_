# routes/generate.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict

from jobs.generate_worker import run_generation
from jobs.job_store import JOB_STORE, JobStatus
from auth.jwt_handler import get_current_user  # your current auth

router = APIRouter()

def map_to_enum_type(t):
    if t == "short":
        return "short_answer"
    return t

class GenerateRequest(BaseModel):
    source_type: str
    text: Optional[str] = None
    document_id: Optional[str] = None
    num_questions: int
    question_types: List[str]
    target_bloom_levels: Optional[List[str]] = None
    target_difficulty_levels: Optional[List[str]] = None
    bloom_distribution: Optional[Dict[str, int]] = None

@router.post("/generate")
async def generate(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user)  # ✅ inject logged-in user
):

    job_id = JOB_STORE.create_job()
    req_payload = request.dict()

    # -------------------------------
    # Attach logged-in user
    # -------------------------------
    req_payload["user_id"] = current_user["id"]

    # -------------------------------
    # Normalize types
    # -------------------------------
    if req_payload.get("question_types"):
        req_payload["question_types"] = [
            map_to_enum_type(t) for t in req_payload["question_types"]
        ]

    # -------------------------------
    # Run background generation
    # -------------------------------
    background_tasks.add_task(
        run_generation,
        job_id,
        req_payload
    )

    return {
        "job_id": job_id,
        "status": JobStatus.PENDING
    }

@router.get("/generate/status/{job_id}")
async def get_status(job_id: str):
    job = JOB_STORE.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"],
        "error": job["error"]
    }