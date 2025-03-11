from pydantic import BaseModel
from typing import List

class ProductBase(BaseModel):
    product_id: str
    name: str
    price: float
    description: str
    stock: int
    image_urls: List[str]
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True