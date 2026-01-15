from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.auth_service import get_current_user
from app.services.listing_service import ListingService
from app.db.session import get_db
from app.schemas.listing import ListingRead
from app.schemas.user import UserRead

# Router for user-related endpoints.
# All routes in this module are grouped under /users.
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    """
    Return the currently authenticated user.

    Authentication is handles by get_current_user, which validates the
    access token and loads the associated user record.
    """
    return current_user


@router.get("/me/listings", response_model=list[ListingRead])
def get_my_listings(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    """
    Retrieve all listings ownded by the authenticated user.

    Listing retrieval is delegated to the listing service, which filters
    listing by the user's ID.
    """
    service = ListingService(db)
    return service.get_listings_by_user(current_user.id)
