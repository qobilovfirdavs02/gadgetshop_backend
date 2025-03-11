from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY  # PostgreSQL uchun, SQLite uchun JSON ishlatamiz
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)  # Maxsus ID
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    stock = Column(Integer)  # Omborda qancha bor
    image_urls = Column(ARRAY(String))  # Cloudinary URL
    category_id = Column(Integer, ForeignKey("categories.id"))  # Kategoriyaga bog‘lash