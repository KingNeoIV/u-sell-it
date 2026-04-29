from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodRead
from app.services.payment_method_service import PaymentMethodService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=PaymentMethodRead)
def add_payment_method(payload: PaymentMethodCreate, 
                       db: Session = Depends(get_db),
                       user=Depends(get_current_user)):
    service = PaymentMethodService(db)
    card = service.add_card(
        user_id=user.id,
        card_number=payload.card_number,
        exp_month=payload.exp_month,
        exp_year=payload.exp_year
    )
    return card

@router.get("/", response_model=list[PaymentMethodRead])
def list_payment_methods(db: Session = Depends(get_db),
                         user=Depends(get_current_user)):
    service = PaymentMethodService(db)
    return service.list_cards(user.id)

@router.delete("/{card_id}")
def delete_payment_method(card_id: str,
                          db: Session = Depends(get_db),
                          user=Depends(get_current_user)):
    service = PaymentMethodService(db)
    ok = service.delete_card(card_id, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Payment method deleted"}
