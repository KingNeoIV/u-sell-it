from pydantic import BaseModel


# Base schema shared by all item-related models.
# Represents the core fields required for an item.
class ItemBase(BaseModel):
    title: str
    description: str | None = None


# Schema used when creating a new item.
# Inherits all fields from ItemBase
class ItemCreate(ItemBase):
    pass


# Schema returned when reading item data from the database.
# Includes identifiers and enables ORM attribute loading.
class ItemRead(ItemBase):
    # Unique indentifier for the item.
    id: int

    # ID of the user who owns the item.
    owner_id: int

    class Config:
        from_attributes = True
