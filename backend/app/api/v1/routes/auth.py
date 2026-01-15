from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import get_user_by_email, create_user
from app.services.auth_service import authenticate_user

# Router for authentication endpoints.
# All routes in this modules are grouped under /auth.
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    The email must be unique. If the email is already registered,
    return a 400 error. User creation, password hashing, and persistence
    are handled in the user service layer.
    """
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_in)


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return access and refresh tokens.

    Credentail validation and token generation are delegated to the
    authentication service. Any authentication failure is raised
    within the sevice layer.
    """
    access_token, refresh_token, _ = authenticate_user(db, login_data)
    return Token(access_token=access_token, refresh_token=refresh_token)
