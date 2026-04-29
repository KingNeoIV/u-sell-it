from pydantic import BaseModel, Field
from uuid import UUID

class PaymentMethodCreate(BaseModel):
    card_number: str = Field(..., min_length=12, max_length=19)
    exp_month: int
    exp_year: int

class PaymentMethodRead(BaseModel):
    id: UUID
    card_brand: str
    last4: str
    exp_month: int
    exp_year: int

    model_config = {
        "from_attributes": True
    }
