from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.image import ImageCreate, ImageRead
from app.services.image_service import ImageService
from app.services.listing_service import ListingService

router = APIRouter()


@router.post("/{listing_id}", response_model=ImageRead)
def add_image(listing_id: str, payload: ImageCreate, db: Session = Depends(get_db)):
    listing_service = ListingService(db)
    if not listing_service.get_listing_by_id(listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")

    image_service = ImageService(db)
    return image_service.add_image(listing_id, payload)
