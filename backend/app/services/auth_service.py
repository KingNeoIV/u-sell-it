from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.services.user_service import get_user_by_email
from app.schemas.auth import LoginRequest
from app.schemas.user import UserRead


def authenticate_user(
    db: Session, login_data: LoginRequest
) -> tuple[str, str, UserRead]:
    user = get_user_by_email(db, login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    user_read = UserRead.model_validate(user)
    return access_token, refresh_token, user_read
