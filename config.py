import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_IvTi7DPg2wOt@ep-restless-dawn-a80hwsr5-pooler.eastus2.azure.neon.tech/gadgetshop_db?sslmode=require")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "6d45eb80e292c7b1a54396f87e5593035bfed8e4cb5c43571e92276bdd0b57a1")
    
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "dwovp8bhl")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "471414582573865")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "soJzEW_5MNJwYhj9IzJS13si6uQ")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set. Please set it in Railway variables.")

settings = Settings()
