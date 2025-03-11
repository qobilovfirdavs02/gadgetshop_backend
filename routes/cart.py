from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cart import Cart as CartModel
from models.user import User as UserModel
from schemas.cart import CartCreate, Cart
from routes.user import get_current_user

router = APIRouter()

@router.post("/cart/", response_model=Cart)
def add_to_cart(cart: CartCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_cart = db.query(CartModel).filter(
        CartModel.user_id == current_user.id,
        CartModel.product_id == cart.product_id
    ).first()
    
    if db_cart:
        db_cart.quantity += cart.quantity
    else:
        db_cart = CartModel(
            user_id=current_user.id,
            product_id=cart.product_id,
            quantity=cart.quantity
        )
        db.add(db_cart)
    
    db.commit()
    db.refresh(db_cart)
    return db_cart

@router.get("/cart/", response_model=list[Cart])
def get_cart(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return db.query(CartModel).filter(CartModel.user_id == current_user.id).all()

@router.delete("/cart/{cart_id}", response_model=dict)
def remove_from_cart(cart_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_cart = db.query(CartModel).filter(CartModel.id == cart_id, CartModel.user_id == current_user.id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Savatchada bunday mahsulot yo‘q")
    db.delete(db_cart)
    db.commit()
    return {"message": "Mahsulot savatchadan o‘chirildi"}