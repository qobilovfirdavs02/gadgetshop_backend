from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    total_price: float
    status: str
    cancel_reason: Optional[str] = None
    created_at: datetime
    product_name: Optional[str] = None  # Optional bilan aniq ixtiyoriy qilindi

    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    status: str
    cancel_reason: Optional[str] = None