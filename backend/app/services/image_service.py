from sqlalchemy.orm import Session
from app.db.models.image import Image
from app.schemas.image import ImageCreate


# Service layer for handling image-related database operations
class ImageService:
    def __init__(self, db: Session):
        # Database session injected from FastAPI dependency.
        self.db = db

    # Createe and persist a new image associated with the listing.
    def add_image(self, listing_id: str, payload: ImageCreate):
        # Construct the Image ORM object using the listing ID and payload data.
        image = Image(listing_id=listing_id, **payload.dict())

        # Persist the new image in the database.
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
