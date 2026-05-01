import uuid
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.models.password_reset_token import PasswordResetToken
from app.core.security import hash_password
from app.core.token_generator import generate_reset_token

class PasswordResetService:
    def __init__(self, db: Session):
        self.db = db

    def create_reset_token(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No account found with this email address"
            ) 

        token = generate_reset_token()

        expires_at = datetime.utcnow() + timedelta(minutes=15)

        reset_entry = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at  
        )

        self.db.add(reset_entry)
        self.db.commit()
        self.db.refresh(reset_entry)
        return reset_entry

    def reset_password(self, token: str, new_password: str):
        entry = (
            self.db.query(PasswordResetToken)
            .filter(PasswordResetToken.token == token)
            .first()
        )

        if not entry or entry.expires_at < datetime.utcnow():
            return None

        user = self.db.query(User).filter(User.id == entry.user_id).first()
        user.hashed_password = hash_password(new_password)

        self.db.delete(entry)
        self.db.commit()
        return user
