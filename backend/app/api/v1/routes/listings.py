from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.listing import ListingCreate, ListingRead
from app.services.listing_service import ListingService

router = APIRouter()


@router.post("/", response_model=ListingRead)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    service = ListingService(db)
    return service.create_listing(payload)


@router.get("/", response_model=list[ListingRead])
def get_listings(
    category_id: str | None = Query(None),
    category_name: str | None = Query(None),
    db: Session = Depends(get_db),
):
    service = ListingService(db)
    return service.get_all_listings(category_id, category_name)


@router.get("/{listing_id}", response_model=ListingRead)
def get_listing(listing_id: str, db: Session = Depends(get_db)):
    service = ListingService(db)
    listing = service.get_listing_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
