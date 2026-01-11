from sqlalchemy.orm import Session
from app.db.models.image import Image
from app.schemas.image import ImageCreate


class ImageService:
    def __init__(self, db: Session):
        self.db = db

    def add_image(self, listing_id: str, payload: ImageCreate):
        image = Image(listing_id=listing_id, **payload.dict())
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
