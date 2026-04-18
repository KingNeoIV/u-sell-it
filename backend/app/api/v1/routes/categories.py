"""
API routes for Category operations.

This module exposes HTTP endpoints for creating, retrieving,
updating, and deleting Category objects. All business logic is
delegated to the CategoryService to keep the routing layer thin
and focused on request/response handling.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter()


@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.

    Delegates creation to the CategoryService. If a category with the same
    name already exists, a 400 Bad Request is returned.
    """
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
    """
    Retrieve a single category by its UUID.

    Returns 404 Not Found if the category does not exist.
    """
    category = CategoryService.get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
    return category


@router.get(
    "",
    response_model=list[CategoryRead],
    summary="Retrieve all categories",
)
def get_all_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    Returns a list of all Category objects stored in the database.
    """
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
    """
    Update an existing category.

    Attempts to update the category with the provided data. If the category
    does not exist, a 404 is returned. If the update violates a uniqueness
    constraint (e.g., duplicate name), a 400 is returned.
    """
    try:
        updated = CategoryService.update_category(db, category_id, data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name must be unique.",
        )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return updated


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a category by its UUID.

    Returns 204 No Content on success. If the category does not exist,
    a 404 Not Found is returned.
    """
    deleted = CategoryService.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )
