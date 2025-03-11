from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # String o'rniga Integer
    product_id = Column(String)
    quantity = Column(Integer)