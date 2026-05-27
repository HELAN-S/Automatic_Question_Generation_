# analytics/schemas.py

from pydantic import BaseModel
from typing import Dict


class AnalyticsSummary(BaseModel):

    total_questions: int

    bloom_distribution: Dict[str, int]

    difficulty_distribution: Dict[str, int]

    question_type_distribution: Dict[str, int]

    avg_relevance: float

    avg_answerability: float

    diversity_score: float

    final_quality_score: float