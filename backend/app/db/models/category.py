import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


# Category model representing item categories within the marketplace.
# Each category has a unique name and an optional description.
class Category(Base):
    __tablename__ = "categories"

    # Primary key using UUID for global uniqueness.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Category name must be unique to prevent duplicates.
    name = Column(String, unique=True, nullable=False)

    # Optional text description providing additional context.
    description = Column(Text, nullable=True)
