import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import admin, product, category, user, order
from database import engine
from models import admin as admin_model, product as product_model, category as category_model, user as user_model, order as order_model


app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "https://gadgetshop-frontend.vercel.app"  # ✅ Vercel frontend domaini qo'shildi
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlar qo'shish
app.include_router(admin.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(order.router)

# Ma'lumotlar bazasi jadvallarini yaratish
admin_model.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
category_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)
order_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "FastAPI server ishlayapti!"}

# ✅ Railway avtomatik `PORT` o'zgaruvchisini oladi
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Railway PORT yoki default 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
