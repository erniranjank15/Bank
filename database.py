import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from models import Users, Accounts

# Load environment variables
load_dotenv()

# Get MongoDB URL
MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is required")

# Create MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)

# Select database (NO parentheses after this)
database = client["bank_db"]


async def init_db():
    """Initialize Beanie with MongoDB"""

    await init_beanie(
        database=database,
        document_models=[Users, Accounts]
    )

    print("✅ Beanie initialized successfully")
