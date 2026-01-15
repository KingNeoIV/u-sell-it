"""
API routes for Category operations.

This module defines the HTTP endpoints for creating, reading,
updating, and deleting Category objects. The routes delegate
business logic to the CategoryService, keeping the API layer
lightweight and maintainable.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return CategoryService.create_category(db, data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists.",
        )


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Retrieve a category by its UUID",
)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = CategoryService.get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )
    return category


@router.get(
    "",
    response_model=list[CategoryRead],
    summary="Retrieve all categories",
)
def get_all_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories(db)


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Update an existing category",
)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated = CategoryService.update_category(db, category_id, data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name must be unique.",
        )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )

    return updated


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    deleted = CategoryService.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
