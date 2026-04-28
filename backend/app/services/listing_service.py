from sqlalchemy.orm import Session
from app.db.models.listing import Listing
from app.db.models.category import Category
from app.schemas.listing import ListingCreate

# Handles all listing-related database operations
class ListingService:
    def __init__(self, db: Session):
        self.db = db

    # Create a new listing
    def create_listing(self, payload: dict):
        listing = Listing(**payload)
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    # Get all active listings, with optional category filters
    def get_all_listings(self, category_id=None, category_name=None):
        query = self.db.query(Listing).filter(Listing.status == "active")

        if category_id:
            query = query.filter(Listing.category_id == category_id)

        if category_name:
            query = query.join(Category).filter(Category.name.ilike(category_name))

        return query.all()

    # Get a single listing by ID
    def get_listing_by_id(self, listing_id: str):
        return self.db.query(Listing).filter(Listing.id == listing_id).first()

    # Get all listings created by a specific user
    def get_listings_by_user(self, user_id: str):
        return self.db.query(Listing).filter(Listing.user_id == user_id).all()

    # Update a listing (blocked if sold)
    def update_listing(self, listing_id: str, payload: dict):
        listing = self.get_listing_by_id(listing_id)
        if not listing or listing.status == "sold":
            return None

        for key, value in payload.items():
            setattr(listing, key, value)

        self.db.commit()
        self.db.refresh(listing)
        return listing

    # Delete a listing (blocked if sold)
    def delete_listing(self, listing_id: str):
        listing = self.get_listing_by_id(listing_id)
        if not listing or listing.status == "sold":
            return None

        self.db.delete(listing)
        self.db.commit()
        return True
