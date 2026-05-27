from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conint
from feedback.feedback_service import submit_feedback

router = APIRouter(prefix="/feedback", tags=["Feedback"])


# Pydantic model ensures usefulness/relevance are integers 1-5
class FeedbackRequest(BaseModel):
    question_id: int
    usefulness: conint(ge=1, le=5)
    relevance: conint(ge=1, le=5)
    comments: str | None = None


@router.post("/submit")
def add_feedback(data: FeedbackRequest):

    try:
        submit_feedback(
            question_id=data.question_id,
            usefulness=data.usefulness,
            relevance=data.relevance,
            comments=data.comments
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save feedback")

    return {"message": "Feedback saved"}