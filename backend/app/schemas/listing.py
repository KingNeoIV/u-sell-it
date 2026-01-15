from pydantic import BaseModel
from typing import Optional, List
from app.schemas.image import ImageRead


# Base schema shared by all listing-related models.
# Represents the core fields required for a markeyplace listing.
class ListingBase(BaseModel):
    title: str
    description: str
    price: float


# Schema used when creating a new listing.
# user_id is optional because it will be injected from the authenticated user.
class ListingCreate(ListingBase):
    user_id: str | None = None


# Schema returned when reading listing data from the database.
# Includes indentifiers and related images.
class ListingRead(ListingBase):
    # Unique identifier for the listing.
    id: str

    # List of images associated with the listing.
    images: List[ImageRead] = []

    class Config:
        orm_mode = True
