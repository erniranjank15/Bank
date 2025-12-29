import motor.motor_asyncio
from beanie import init_beanie
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string - will use environment variable in production
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "bank_system")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is required")

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

async def init_db():
    """Initialize database with Beanie ODM"""
    from models import Users, Accounts
    
    await init_beanie(
        database=database,
        document_models=[Users, Accounts]
    )

def get_database():
    """Get database instance"""
    return database
