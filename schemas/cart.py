from pydantic import BaseModel

class CartCreate(BaseModel):
    product_id: str
    quantity: int

class Cart(BaseModel):
    id: int
    user_id: str
    product_id: str
    quantity: int

    class Config:
        orm_mode = True