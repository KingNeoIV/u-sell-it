from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


# Item model representing a user-ownd item in the marketplace.
# Each item includes a title, optional description, and an owner reference.
class Item(Base):
    __tablename__ = "items"

    # Primary key using an integer sequence.
    id = Column(Integer, primary_key=True, index=True)

    # Short title decribing the item.
    title = Column(String(255), nullable=False)

    # Optional detailed description of the item.
    description = Column(Text, nullable=True)

    # Foreign key linking the item to its owner (User model).
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
