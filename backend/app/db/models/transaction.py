import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base

# Transaction model representing a purchase event between a buyer and seller.
# Each transaction links two users and the listing being purchased.
class Transaction(Base):
    __tablename__ = "transactions"

    # Primary key using UUID for global uniqueness
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # User initiating the purchase.
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # User selling the item.
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Listing being purchased.
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)

    # Payment method used for the transaction.
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods.id"), nullable=False)

    # Total amount charged to the buyer.
    amount = Column(Numeric(10, 2), nullable=False)

    # Marketplace fee charged.
    fee_amount = Column(Numeric(10, 2), nullable=False)

    # Amount the seller will receive.
    seller_amount = Column(Numeric(10, 2), nullable=False)

    # Current transaction status (paid, refunded, etc.).
    status = Column(String, default="paid")

    # Timestamp automatically set when the transaction is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
