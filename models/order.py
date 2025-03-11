from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String, default="pending")  # pending, accepted, cancelled
    cancel_reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())