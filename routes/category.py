from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.category import Category as CategoryModel
from schemas.category import CategoryCreate, Category

router = APIRouter()

@router.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryModel).all()