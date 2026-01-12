from pydantic import BaseModel
from typing import Optional, List
from app.schemas.image import ImageRead


class ListingBase(BaseModel):
    title: str
    description: str
    price: float


class ListingCreate(ListingBase):
    user_id: str | None = None


class ListingRead(ListingBase):
    id: str
    images: List[ImageRead] = []

    class Config:
        orm_mode = True
