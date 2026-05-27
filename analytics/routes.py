from fastapi import APIRouter
from analytics.aggregator import aggregate_questions
from analytics.schemas import AnalyticsSummary
from typing import List, Dict

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/summary", response_model=AnalyticsSummary)
def get_summary(questions: List[Dict]):
    return aggregate_questions(questions)