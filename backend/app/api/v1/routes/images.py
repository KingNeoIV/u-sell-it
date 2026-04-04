from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.image import ImageRead
from app.services.image_service import ImageService
from app.services.listing_service import ListingService

# Router for image-related operations.
# These endpoints handle attaching images to existing listings.
router = APIRouter()


@router.post("/{listing_id}", response_model=ImageRead)
def add_image(
    listing_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Attach an image to a listing.

    The listing must exist before an image can be added.
    If the listing is not found, return a 404 error.
    Image creation and persistence are delegated to the image service layer.
    """
    listing_service = ListingService(db)
    if not listing_service.get_listing_by_id(listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")

    image_service = ImageService(db)
    return image_service.add_image(listing_id, file)
