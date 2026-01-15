from uuid import UUID
from pydantic import BaseModel, EmailStr


# Base schema shared by all user-related models.
# Represents the core identity field for a user.
class UserBase(BaseModel):
    email: EmailStr


# Schema used when creating a new user.
# Includes the plaintext password before hashing.
class UserCreate(UserBase):
    password: str


# Schema returned when reading user data from the database.
# Includes identifiers and account status.
class UserRead(UserBase):
    # Unique identifier for the user.
    id: UUID

    # Indicates whether the user account is active.
    is_active: bool

    class Config:
        from_attributes = True
