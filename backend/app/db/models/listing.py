import uuid
from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


# Listing model representing an item posted for sale in the marketplace.
# Each listing includes metadata, pricing, ownership, and related images.
class Listing(Base):
    __tablename__ = "listings"

    # Primary key using UUID for global uniqueness.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Title of the listing, required for all items.
    title = Column(String, nullable=False)

    # Optional detailed description of the item.
    description = Column(Text)

    # Price stored as a fixed-precision numeric value.
    price = Column(Numeric(10, 2), nullable=False)

    # Foreign key linking the listing to the user who created it.
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Foreign key linking the listing to its category.
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)

    # Timestamp automatically set when the listing is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to the User model (owner of the listing).
    user = relationship("User", backref="listings")

    # Relationship to associated Image records.
    images = relationship("Image", backref="listing")
