import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "bank_system")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

async def init_db():
    from models import Users, Accounts, PasswordResetOTP

    await init_beanie(
        database=database,  # ✅ no ()
        document_models=[Users, Accounts, PasswordResetOTP]
    )

def get_database():
    return database
