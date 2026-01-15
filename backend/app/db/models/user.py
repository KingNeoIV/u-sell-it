import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base


# User model representing registered users in the system.
# Stores authentication details and account creation metadata.
class User(Base):
    __tablename__ = "users"

    # Primary key using UUID for global uniqueness.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Unique email address used for login and indentification.
    email = Column(String, unique=True, index=True, nullable=False)

    # Securely hashed password (bcrypt via Passlib).
    hashed_password = Column(String, nullable=False)

    # Timestamp automatically set when the user account is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
