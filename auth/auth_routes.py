#auth/auth_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth.auth_utils import create_token, hash_password, verify_password
from auth.user_repository import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str
@router.post("/register")
def register(data: RegisterRequest):

    if len(data.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer"
        )

    existing = get_user_by_email(data.email)

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(data.password)

    create_user(data.name, data.email, hashed)

    return {"message": "User registered successfully"}




@router.post("/login")
def login(data: LoginRequest):

    user = get_user_by_email(data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user["email"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }