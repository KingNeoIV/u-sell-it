from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.listing import ListingCreate, ListingRead
from app.services.listing_service import ListingService
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/", response_model=ListingRead)
def create_listing(
    payload: ListingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new listing.

    The authenticated user becomes the owner of the listing.
    Listing creation and persistence are handled in the service layer.
    """
    service = ListingService(db)

    data = payload.model_dump()
    data["user_id"] = str(current_user.id)

    return service.create_listing(data)


@router.get("/", response_model=list[ListingRead])
def get_listings(
    category_id: str | None = Query(None),
    category_name: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Retrieve all listings with optional category filtering.

    Both category_id and category_name are optional filters.
    Filtering and query logic are delegated to the service layer.
    """
    service = ListingService(db)
    return service.get_all_listings(category_id, category_name)


@router.get("/{listing_id}", response_model=ListingRead)
def get_listing(listing_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single listing by its ID.

    If the listing does not exist, return a 404 error.
    """
    service = ListingService(db)
    listing = service.get_listing_by_id(listing_id)

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    return listing


@router.put("/{listing_id}", response_model=ListingRead)
def update_listing(
    listing_id: str,
    payload: ListingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update an existing listing.

    The listing must exist and must belong to the authenticated user.
    Unauthorized users receive a 403 error.
    """
    service = ListingService(db)
    listing = service.get_listing_by_id(listing_id)

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this listing"
        )

    update = service.update_listing(listing_id, payload.dict(exclude_unset=True))
    return update


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete an existing listing.

    The listing must exist and must be owned by the authenticated user.
    A successful deletion returns a 204 No Content response.
    """
    service = ListingService(db)
    listing = service.get_listing_by_id(listing_id)

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this listing"
        )

    service.delete_listing(listing_id)
    return None
