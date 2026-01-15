import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime
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

    # Current transaction status (pending, completed, cancelled, etc.).
    status = Column(String, default="pending")

    # Timestamp automatically set when the transaction is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
