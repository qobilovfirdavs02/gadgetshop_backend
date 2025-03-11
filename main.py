import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import admin, product, category, user, order
from database import engine
from models import admin as admin_model, product as product_model, category as category_model, user as user_model, order as order_model
import cloudinary




cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(admin.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(order.router)

admin_model.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
category_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)
order_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "FastAPI server ishlayapti!"}
