from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.transaction import Transaction
from app.db.models.listing import Listing
from app.schemas.transaction import TransactionCreate

# Get a single transaction
def get_transaction(db: Session, transaction_id):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

# List all transactions
def list_transactions(db: Session):
    return db.query(Transaction).all()

# List all purchases for a user
def get_purchases_by_user(db: Session, user_id: str):
    return db.query(Transaction).filter(Transaction.buyer_id == user_id).all()

# List all sales for a user
def get_sales_by_user(db: Session, user_id: str):
    return (
        db.query(Transaction)
        .join(Listing, Transaction.listing_id == Listing.id)
        .filter(Listing.user_id == user_id)
        .all()
    )

# Pay for a listing (buyer purchases a listing using a saved payment method)
def pay_for_listing_service(
    db: Session,
    listing,
    buyer_id,
    payment_method
):
    # 1. Calculate financials
    price = listing.price  # Decimal
    fee = (price * Decimal("0.05")).quantize(Decimal("0.01"))
    seller_amount = (price - fee).quantize(Decimal("0.01"))

    # 2. Create transaction record
    tx = Transaction(
        buyer_id=buyer_id,
        seller_id=listing.user_id,
        listing_id=listing.id,
        payment_method_id=payment_method.id,
        amount=price,
        fee_amount=fee,
        seller_amount=seller_amount,
        status="paid",
    )

    # 3. Mark listing as sold
    listing.status = "sold"

    # 4. Commit changes
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return tx
