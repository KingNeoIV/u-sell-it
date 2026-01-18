from pydantic import BaseModel
from typing import Optional, List
from app.schemas.image import ImageRead
from uuid import UUID


# Base schema shared by all listing-related models.
# Represents the core fields required for a markeyplace listing.
class ListingBase(BaseModel):
    title: str
    description: str
    price: float


# Schema used when creating a new listing.
# category_id allows the listing to be assigned to a category, but is not required.
class ListingCreate(ListingBase):
    category_id: str


# Schema returned when reading listing data from the database.
# Includes indentifiers and related images.
class ListingRead(ListingBase):
    # Unique identifier for the listing.
    id: UUID

    # List of images associated with the listing.
    images: List[ImageRead] = []

    model_config = {"from_attributes": True}
