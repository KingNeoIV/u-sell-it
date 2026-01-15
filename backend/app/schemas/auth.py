from pydantic import BaseModel, EmailStr


# Schema for login requests.
# Validates user credentials submitted during authentication.
class LoginRequest(BaseModel):
    # User email address, validated using Pydantic's EmailStr.
    email: EmailStr

    # Plaintext password provided by the user.
    password: str


# Schema returned after successful authentication.
# Contains both access and refresh tokens for the client.
class Token(BaseModel):
    # Short-lived JWT used for authenticated API requests.
    access_token: str

    # Long-lived JWT used to obtain new access tokens.
    refresh_token: str

    # Token type used in Authorization headers.
    token_type: str = "bearer"
