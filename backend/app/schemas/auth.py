from uuid import UUID
from pydantic import BaseModel, EmailStr


# Public user representation returned to the client
class UserPublic(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        from_attributes = True


# Schema for login requests
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Schema returned after successful authentication (tokens only)
# This is still useful for refresh endpoints
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Modern login response: tokens + user object
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic
