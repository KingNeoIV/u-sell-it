from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Shared fields for all transaction schemas
class TransactionBase(BaseModel):
    buyer_id: UUID
    seller_id: UUID
    listing_id: UUID
    status: str = "pending"

# Schema for creating a new transaction
class TransactionCreate(TransactionBase):
    pass

# Schema returned in API responses
class Transaction(TransactionBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
