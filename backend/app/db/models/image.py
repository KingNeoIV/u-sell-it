import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


# Image model representing file paths associated with a listing.
# Each image belongs to a specific listing through a foreign key.
class Image(Base):
    __tablename__ = "images"

    # Primary key using UUID for global uniqueness.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key linking the image to its parent listing.
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)

    # Path to the stored image file.
    file_path = Column(String, nullable=False)
