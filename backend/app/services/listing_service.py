from sqlalchemy.orm import Session
from app.db.models.listing import Listing
from app.schemas.listing import ListingCreate


class ListingService:
    def __init__(self, db: Session):
        self.db = db

    def create_listing(self, payload: ListingCreate):
        listing = Listing(**payload.dict())
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def get_all_listings(self):
        return self.db.query(Listing).all()

    def get_listing_by_id(self, listing_id: str):
        return self.db.query(Listing).filter(Listing.id == listing_id).first()
