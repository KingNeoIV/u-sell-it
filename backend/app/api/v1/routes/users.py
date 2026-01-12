from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.auth_service import get_current_user
from app.services.listing_service import ListingService
from app.db.session import get_db
from app.schemas.listing import ListingRead
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/me/listings", response_model=list[ListingRead])
def get_my_listings(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    service = ListingService(db)
    return service.get_listings_by_user(current_user.id)
