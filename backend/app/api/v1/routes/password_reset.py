from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest
from app.services.password_reset_service import PasswordResetService

router = APIRouter()

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    service = PasswordResetService(db)
    token = service.create_reset_token(payload.email)

    # Simulation: return token directly
    return {"message": "Password reset link generated (simulation)", 
            "token": token,
            "expires_in_minutes": 15}

@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    service = PasswordResetService(db)
    user = service.reset_password(payload.token, payload.new_password)

    if not user:
        return {"message": "Invalid or expired token"}

    return {"message": "Password updated successfully"}
