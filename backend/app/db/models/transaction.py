import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
