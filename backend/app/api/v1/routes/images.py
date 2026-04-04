from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.image import ImageRead
from app.services.image_service import ImageService
from app.services.listing_service import ListingService

# Router for image-related operations.
router = APIRouter(tags=["images"])


@router.post("/{listing_id}", response_model=ImageRead)
async def add_image(
    listing_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Attach an image to a listing.

    The listing must exist before an image can be added.
    If the listing is not found, return a 404 error.
    Image creation and persistence are delegated to the image service layer.
    """

    # Ensure listing exists
    listing_service = ListingService(db)
    if not listing_service.get_listing_by_id(str(listing_id)):
        raise HTTPException(status_code=404, detail="Listing not found")

    # Save image using the service
    image_service = ImageService(db)
    image = await image_service.add_image(str(listing_id), file)

    return image
