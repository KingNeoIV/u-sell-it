from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.transaction import Transaction, TransactionCreate
from app.services.transaction_service import (
    create_transaction,
    get_transaction,
    list_transactions,
)

router = APIRouter()

# Create a new transaction (buyer purchases a listing)
@router.post("/", response_model=Transaction)
def create(data: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, data)

# Get a single transaction by ID
@router.get("/{transaction_id}", response_model=Transaction)
def get(transaction_id: UUID, db: Session = Depends(get_db)):
    return get_transaction(db, transaction_id)

# List all transactions
@router.get("/", response_model=list[Transaction])
def list_all(db: Session = Depends(get_db)):
    return list_transactions(db)
