from sqlalchemy.orm import Session
from app.db.models.listing import Listing
from app.db.models.category import Category
from app.schemas.listing import ListingCreate


# Service layer for handling listing-related database operations.
class ListingService:
    def __init__(self, db: Session):
        # Database session injected from FastAPI dependency.
        self.db = db

    # Create and persist a new listing.
    def create_listing(self, payload: ListingCreate):
        # Construct the Listing ORM object from the payload.
        listing = Listing(**payload.dict())

        # Persist the new listing in the database.
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    # Retieve all listing, optionally filtered by category ID or category name.
    def get_all_listings(self, category_id=None, category_name=None):
        query = self.db.query(Listing)

        # Filter by category ID if provided.
        if category_id:
            query = query.filter(Listing.category_id == category_id)

        # Filter by category name using a case-insensitive match.
        if category_name:
            query = query.join(Category).filter(Category.name.ilike(category_name))

        return query.all()

    # Retrieve a single listing by its ID.
    def get_listing_by_id(self, listing_id: str):
        return self.db.query(Listing).filter(Listing.id == listing_id).first()

    # Retrieve all listings created by a specific user.
    def get_listings_by_user(self, user_id: str):
        return self.db.query(Listing).filter(Listing.user_id == user_id).all()

    # Update an existing listing with new field values.
    def update_listing(self, listing_id: str, payload: dict):
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            return None

        # Apply updates to the listing object.
        for key, value in payload.items():
            setattr(listing, key, value)

        self.db.commit()
        self.db.refresh(listing)
        return listing

    # Delete a listing by its ID.
    def delete_listing(self, listing_id: str):
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            return None

        self.db.delete(listing)
        self.db.commit()
        return True
