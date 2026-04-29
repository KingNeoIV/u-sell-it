from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.transaction import Transaction, TransactionCreate
from app.services.transaction_service import (
    get_transaction,
    list_transactions,
    get_purchases_by_user,
    get_sales_by_user,
    pay_for_listing_service,
)
from app.services.listing_service import ListingService
from app.services.payment_method_service import PaymentMethodService
from app.services.auth_service import get_current_user

router = APIRouter()

# Get a single transaction
@router.get("/{transaction_id}", response_model=Transaction)
def get(transaction_id: UUID, db: Session = Depends(get_db)):
    return get_transaction(db, transaction_id)

# List all transactions
@router.get("/", response_model=list[Transaction])
def list_all(db: Session = Depends(get_db)):
    return list_transactions(db)

# List all purchases for a user
@router.get("/purchases/{user_id}", response_model=list[Transaction])
def purchases(user_id: str, db: Session = Depends(get_db)):
    return get_purchases_by_user(db, user_id)

# List all sales for a user
@router.get("/sales/{user_id}", response_model=list[Transaction])
def sales(user_id: str, db: Session = Depends(get_db)):
    return get_sales_by_user(db, user_id)

# Pay for a listing
@router.post("/pay/{listing_id}", response_model=Transaction)
def pay_for_listing(
    listing_id: UUID,
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 1. Validate listing
    listing_service = ListingService(db)
    listing = listing_service.get_listing_by_id(listing_id)

    if not listing:
        raise HTTPException(404, "Listing not found")

    if listing.user_id == user.id:
        raise HTTPException(400, "You cannot buy your own listing")

    if listing.status != "active":
        raise HTTPException(400, "Listing is not available")

    # 2. Validate payment method
    pm_service = PaymentMethodService(db)
    payment_method = pm_service.get_payment_method(user.id, payload.payment_method_id)
    if not payment_method:
        raise HTTPException(404, "Payment method not found")

    # 3. Process payment
    tx = pay_for_listing_service(
        db=db,
        listing=listing,
        buyer_id=user.id,
        payment_method=payment_method
    )

    return tx
