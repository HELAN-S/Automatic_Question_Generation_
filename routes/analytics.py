# routes/analytics.py
from fastapi import APIRouter
from typing import Dict

from analytics.aggregator import aggregate_questions
from analytics.schemas import AnalyticsSummary

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.post(
    "/summary",
    response_model=AnalyticsSummary
)
def get_analytics_summary(data: Dict):

    return aggregate_questions(data)