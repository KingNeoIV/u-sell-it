from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest
from app.services.password_reset_service import PasswordResetService

router = APIRouter()

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    service = PasswordResetService(db)
    
    # service.create_reset_token now raises 404 automatically if email is missing
    reset_entry = service.create_reset_token(payload.email)

    return {
        "message": "Password reset link generated (simulation)", 
        "token": reset_entry.token,
        "expires_at": reset_entry.expires_at.isoformat() # This sends the real timestamp
    }

@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    service = PasswordResetService(db)
    user = service.reset_password(payload.token, payload.new_password)

    # Throw a 400 error instead of a 200 message for invalid tokens
    # This helps your Frontend 'catch' the error properly
    if not user:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    return {"message": "Password updated successfully"}
