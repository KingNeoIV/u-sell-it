from app.db.models.payment_method import PaymentMethod
from sqlalchemy.orm import Session

def detect_brand(card_number: str) -> str:
    if card_number.startswith("4"):
        return "Visa"
    if card_number.startswith("5"):
        return "Mastercard"
    if card_number.startswith("3"):
        return "American Express"
    return "Unknown"

class PaymentMethodService:
    def __init__(self, db: Session):
        self.db = db

    def add_card(self, user_id, card_number, exp_month, exp_year):
        brand = detect_brand(card_number)
        last4 = card_number[-4:]

        card = PaymentMethod(
            user_id=user_id,
            card_brand=brand,
            last4=last4,
            exp_month=exp_month,
            exp_year=exp_year
        )

        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def list_cards(self, user_id):
        return self.db.query(PaymentMethod).filter_by(user_id=user_id).all()

    def delete_card(self, card_id, user_id):
        card = self.db.query(PaymentMethod).filter_by(id=card_id, user_id=user_id).first()
        if not card:
            return False
        self.db.delete(card)
        self.db.commit()
        return True
