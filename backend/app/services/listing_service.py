from sqlalchemy.orm import Session
from app.db.models.listing import Listing
from app.db.models.category import Category
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

    def get_all_listings(self, category_id=None, category_name=None):
        query = self.db.query(Listing)

        if category_id:
            query = query.filter(Listing.category_id == category_id)

        if category_name:
            query = query.join(Category).filter(Category.name.ilike(category_name))

        return query.all()

    def get_listing_by_id(self, listing_id: str):
        return self.db.query(Listing).filter(Listing.id == listing_id).first()

    def get_listings_by_user(self, user_id: str):
        return self.db.query(Listing).filter(Listing.user_id == user_id).all()

    def update_listing(self, listing_id: str, payload: dict):
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            return None

        for key, value in payload.items():
            setattr(listing, key, value)

        self.db.commit()
        self.db.refresh(listing)
        return listing

    def delete_listing(self, listing_id: str):
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            return None

        self.db.delete(listing)
        self.db.commit()
        return True
