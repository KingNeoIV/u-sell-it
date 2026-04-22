"""
Service layer for Category operations.

This module contains reusable business logic for creating, reading,
updating, and deleting Category objects. The service layer keeps
database operations separate from the API routes, which improves
maintainability and testability.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """
    Provides CRUD operations for Category objects.
    All methods are static because the service does not maintain state.
    """

    @staticmethod
    def create_category(db: Session, data: CategoryCreate) -> Category:
        """
        Create a new Category.

        Args:
            db: Active SQLAlchemy database session.
            data: Validated CategoryCreate schema containing input fields.

        Returns:
            The newly created Category object.

        Raises:
            IntegrityError: If a category with the same name already exists.
        """
        category = Category(name=data.name, description=data.description)

        db.add(category)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(category)
        return category

    @staticmethod
    def get_category(db: Session, category_id: UUID) -> Optional[Category]:
        """
        Retrieve a single Category by its UUID.

        Args:
            db: Active SQLAlchemy session.
            category_id: UUID of the category to retrieve.

        Returns:
            The Category object if found, otherwise None.
        """
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_all_categories(db: Session) -> List[Category]:
        """
        Retrieve all categories in the system.

        Args:
            db: Active SQLAlchemy session.

        Returns:
            A list of all Category objects.
        """
        return db.query(Category).order_by(Category.name.asc()).all()

    @staticmethod
    def update_category(
        db: Session, category_id: UUID, data: CategoryUpdate
    ) -> Optional[Category]:
        """
        Update an existing Category.

        Args:
            db: Active SQLAlchemy session.
            category_id: UUID of the category to update.
            data: CategoryUpdate schema containing updated fields.

        Returns:
            The updated Category object if found, otherwise None.

        Raises:
            IntegrityError: If updating the name violates the unique constraint.
        """
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return None

        # Apply only fields that were provided
        if data.name is not None:
            category.name = data.name

        if data.description is not None:
            category.description = data.description

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: UUID) -> bool:
        """
        Delete a Category by its UUID.

        Prevents deletion if any listings are still associated with the category.
        """
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return False

        # Prevent deletion if listings reference this category
        if category.listings and len(category.listings) > 0:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail="Category cannot be deleted because it has associated listings"
            )

        db.delete(category)
        db.commit()
        return True


        db.delete(category)
        db.commit()
        return True
