#profile_routes.py
from fastapi import APIRouter, Depends, HTTPException
from auth.dependencies import get_current_user
from auth.user_repository import get_user_by_email

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me")
def get_profile(user_email: str = Depends(get_current_user)):

    user = get_user_by_email(user_email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": user["name"],
        "email": user["email"]
    }