from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from auth.auth_utils import SECRET_KEY, ALGORITHM
from auth.user_repository import get_user_by_email

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = get_user_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user   # contains id, email, name

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )