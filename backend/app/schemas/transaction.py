from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# -----------------------------
# TransactionCreate
# -----------------------------
# What the buyer sends when paying for a listing.
class TransactionCreate(BaseModel):
    payment_method_id: UUID


# -----------------------------
# Transaction (read model)
# -----------------------------
# What the API returns.
class Transaction(BaseModel):
    id: UUID
    buyer_id: UUID
    seller_id: UUID
    listing_id: UUID
    payment_method_id: UUID

    amount: float
    fee_amount: float
    seller_amount: float

    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
