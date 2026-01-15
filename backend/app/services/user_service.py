from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


# Retrieve a user by their email address.
# Returns None if no matching user exists.
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


# Retrieve a user by their ID.
# Returns None if the user does not exist.
def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


# Create a new user with a securely hashed password.
# Return the newly created User ORM object.
def create_user(db: Session, user_in: UserCreate) -> User:
    # Hash the plaintext password before storing it.
    hashed_pw = hash_password(user_in.password)

    # Construct the User ORM object.
    user = User(email=user_in.email, hashed_password=hashed_pw)

    # Persist the new user in the database.
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
