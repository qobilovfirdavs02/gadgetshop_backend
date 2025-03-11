from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.admin import Admin as AdminModel
from schemas.admin import AdminCreate, Admin
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Login uchun Pydantic modeli
class AdminLogin(BaseModel):
    username: str
    password: str

@router.post("/admins/", response_model=Admin)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(admin.password)
    db_admin = AdminModel(username=admin.username, email=admin.email, password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@router.post("/admin/login/")
def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(AdminModel).filter(AdminModel.username == admin.username).first()
    if not db_admin or not pwd_context.verify(admin.password, db_admin.password):
        raise HTTPException(status_code=401, detail="Noto‘g‘ri username yoki parol")
    return {"message": "Login muvaffaqiyatli", "admin_id": db_admin.id}