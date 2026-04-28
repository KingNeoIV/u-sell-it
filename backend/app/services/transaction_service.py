from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.transaction import Transaction
from app.db.models.listing import Listing
from app.schemas.transaction import TransactionCreate

# Create a new transaction and update listing status
def create_transaction(db: Session, data: TransactionCreate):
    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")

    if listing.user_id == data.buyer_id:
        raise HTTPException(status_code=400, detail="You cannot buy your own listing.")

    if listing.status == "sold":
        raise HTTPException(status_code=400, detail="Listing is already sold.")

    transaction = Transaction(**data.dict())
    db.add(transaction)

    listing.status = "sold"

    db.commit()
    db.refresh(transaction)
    return transaction

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
