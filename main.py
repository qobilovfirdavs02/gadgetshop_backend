from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import admin, product, category, user, order
from database import engine
from models import admin as admin_model, product as product_model, category as category_model, user as user_model, order as order_model
import cloudinary

app = FastAPI()

origins = [
    "http://localhost:5173",              # Local development
    "https://gadgetshop-frontend.vercel.app"  # Vercel’dagi React URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cloudinary.config(
    cloud_name="dwovp8bhl",  # Dashboard’dan oling
    api_key="471414582573865",     # Siz bergan API key
    api_secret="your_api_secret"   # Dashboard’dan olingan secret
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
