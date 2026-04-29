import secrets
import string

def generate_reset_token(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))
