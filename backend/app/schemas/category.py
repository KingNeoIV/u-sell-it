"""
Pydantic schemas for Category objects.

These schemas define how Category data is validated and transferred
between the API layer and the database layer. They ensure that incoming
requests contain valid fields and that outgoing resposes follow a
consistent structure.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """
    Shared fields used by multiple Category schemas.
    This includes attributes that can be provided by the client.
    """

    name: str = Field(..., description="Readable name of category must be unique.")
    description: Optional[str] = Field(
        None,
        description="Optional text describing the purpose or context of the category.",
    )


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new Category.
    Inherits all fields from CategoryBase.
    """

    pass


class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing Category.
    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(
        None, description="Update category name. Must remain unique."
    )
    description: Optional[str] = Field(
        None, description="Update description for the category."
    )


class CategoryRead(CategoryBase):
    """
    Schema returned when reading Category data from the API.
    Includes the UUID primary key.
    """

    id: UUID = Field(..., description="Unique identifier for the category.")

    class Config:
        from_attributes = True
