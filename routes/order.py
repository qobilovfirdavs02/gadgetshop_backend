from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.order import Order as OrderModel
from models.user import User as UserModel
from models.product import Product as ProductModel
from schemas.order import OrderCreate, Order, OrderUpdate
from routes.user import get_current_user

router = APIRouter()

@router.post("/orders/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    product = db.query(ProductModel).filter(ProductModel.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Omborda yetarli mahsulot yo‘q")
    
    total_price = product.price * order.quantity
    db_order = OrderModel(
        user_id=current_user.id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db_order.product_name = product.name  # Javobda product_name qo‘shildi
    return db_order

@router.get("/orders/", response_model=list[Order])
def get_orders(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    orders = db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()
    for order in orders:
        product = db.query(ProductModel).filter(ProductModel.id == order.product_id).first()
        order.product_name = product.name if product else "Noma’lum"
    return orders

@router.get("/admin/orders/", response_model=list[Order])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).all()
    for order in orders:
        product = db.query(ProductModel).filter(ProductModel.id == order.product_id).first()
        order.product_name = product.name if product else "Noma’lum"
    return orders

@router.put("/admin/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    
    if order_update.status == "cancelled" and not order_update.cancel_reason:
        raise HTTPException(status_code=400, detail="Bekor qilish sababi majburiy")
    
    db_order.status = order_update.status
    if order_update.cancel_reason:
        db_order.cancel_reason = order_update.cancel_reason
    db.commit()
    db.refresh(db_order)
    product = db.query(ProductModel).filter(ProductModel.id == db_order.product_id).first()
    db_order.product_name = product.name if product else "Noma’lum"
    return db_order

@router.put("/orders/{order_id}", response_model=Order)
def user_cancel_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.user_id == current_user.id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi yoki sizga tegishli emas")
    if db_order.status != "pending":
        raise HTTPException(status_code=400, detail="Faqat tasdiqlanmagan buyurtmani bekor qilish mumkin")
    
    db_order.status = order_update.status
    if order_update.cancel_reason:
        db_order.cancel_reason = order_update.cancel_reason
    db.commit()
    db.refresh(db_order)
    product = db.query(ProductModel).filter(ProductModel.id == db_order.product_id).first()
    db_order.product_name = product.name if product else "Noma’lum"
    return db_order