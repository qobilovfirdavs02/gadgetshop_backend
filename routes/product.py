from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product as ProductModel
from schemas.product import ProductCreate, Product

router = APIRouter()

@router.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if db.query(ProductModel).filter(ProductModel.product_id == product.product_id).first():
        raise HTTPException(status_code=400, detail="Bu product_id band")
    
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    return products

@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    return product

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    db.delete(db_product)
    db.commit()
    return {"message": "Mahsulot o‘chirildi"}