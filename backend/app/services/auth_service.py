from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.services.user_service import get_user_by_email
from app.services.user_service import get_user_by_id
from app.schemas.auth import LoginRequest
from app.schemas.user import UserRead
import uuid

# Use simple Bearer token authentication for Swagger and protected routes.
oauth2_scheme = HTTPBearer()


# Authenticate a user using email and password.
# Returns an access token, refresh token, and a serialized user object.
def authenticate_user(
    db: Session, login_data: LoginRequest
) -> tuple[str, str, UserRead]:

    # Look up the user my email.
    user = get_user_by_email(db, login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Verify the provided password against the stored hash.
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Generate JWT access and refresh tokens.
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    # Convert ORM user object into a Pydantic schema.
    user_read = UserRead.model_validate(user)
    return access_token, refresh_token, user_read


# Retrive the currently authenticated user from a JWT token.
# Used as a dependency in protected routes.
def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extract the raw token string from HTTPAuthorizationCredentials
        token_str = token.credentials

        # Decode the JWT and extract the subject (user ID)
        payload = jwt.decode(
            token_str,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        # Convert string UUID to actual UUID object
        user_id = uuid.UUID(user_id_str)

    except (JWTError, ValueError):
        raise credentials_exception

    # Look up the user in the database.
    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user
