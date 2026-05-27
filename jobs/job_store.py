# jobs/job_store.py

import uuid
from enum import Enum
from typing import Dict, Any


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobStore:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def create_job(self, job_id: str = None) -> str:
        if job_id is None:
            job_id = str(uuid.uuid4())

        self.store[job_id] = {
            "status": JobStatus.PENDING,
            "result": None,
            "error": None
        }
        return job_id

    def set_running(self, job_id: str):
        if job_id in self.store:
            self.store[job_id]["status"] = JobStatus.RUNNING

    def complete_job(self, job_id: str, result: Any):
        if job_id in self.store:
            self.store[job_id]["status"] = JobStatus.COMPLETED
            self.store[job_id]["result"] = result
            self.store[job_id]["error"] = None

    def fail_job(self, job_id: str, error: str):
        if job_id in self.store:
            self.store[job_id]["status"] = JobStatus.FAILED
            self.store[job_id]["error"] = error
            self.store[job_id]["result"] = None

    def get_job(self, job_id: str):
        return self.store.get(job_id)


# 🔥 Global instance
JOB_STORE = JobStore()