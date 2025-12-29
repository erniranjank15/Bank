from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime
from pymongo import IndexModel, ReturnDocument


class Counter(Document):
    """Counter collection for auto-increment IDs"""
    collection_name: str = Field(..., unique=True)
    sequence_value: int = Field(default=0)
    
    class Settings:
        name = "counters"


class Users(Document):
    user_id: int = Field(..., unique=True)  # Auto-increment ID
    username: str = Field(..., unique=True)
    hashed_password: str
    email: EmailStr = Field(..., unique=True)
    mob_no: int = Field(..., unique=True)
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            IndexModel("user_id", unique=True),
            IndexModel("username", unique=True),
            IndexModel("email", unique=True),
            IndexModel("mob_no", unique=True),
        ]
    
    @classmethod
    async def get_next_id(cls) -> int:
        """Get next auto-increment ID with fallback mechanism"""
        try:
            # Method 1: Use MongoDB atomic operations (preferred)
            from database import get_database
            
            db = get_database()
            result = await db.counters.find_one_and_update(
                {"collection_name": "users"},
                {"$inc": {"sequence_value": 1}},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            
            return result["sequence_value"]
            
        except Exception as e:
            # Method 2: Fallback to Beanie with retry logic
            print(f"MongoDB atomic operation failed, using fallback: {e}")
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    counter = await Counter.find_one(Counter.collection_name == "users")
                    
                    if not counter:
                        # Create new counter
                        counter = Counter(collection_name="users", sequence_value=1)
                        await counter.insert()
                        return 1
                    else:
                        # Increment existing counter
                        counter.sequence_value += 1
                        await counter.save()
                        return counter.sequence_value
                        
                except Exception as retry_error:
                    if attempt == max_retries - 1:
                        # Final fallback: use timestamp-based ID
                        import time
                        fallback_id = int(time.time()) % 100000
                        print(f"All methods failed, using timestamp fallback: {fallback_id}")
                        return fallback_id
                    
                    # Wait before retry
                    import asyncio
                    await asyncio.sleep(0.1)


class Accounts(Document):
    acc_no: int = Field(..., unique=True)  # Auto-increment ID
    acc_holder_name: str
    acc_holder_address: str
    dob: str
    gender: str
    acc_type: str
    balance: float = Field(default=100.0)
    ifsc_code: int = Field(default=123456)
    branch: str = Field(default="Main Branch")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Reference to user using user_id instead of ObjectId
    user_id: int
    
    class Settings:
        name = "accounts"
        indexes = [
            IndexModel("acc_no", unique=True),
            IndexModel("user_id"),
        ]
    
    @classmethod
    async def get_next_id(cls) -> int:
        """Get next auto-increment ID with fallback mechanism"""
        try:
            # Method 1: Use MongoDB atomic operations (preferred)
            from database import get_database
            
            db = get_database()
            result = await db.counters.find_one_and_update(
                {"collection_name": "accounts"},
                {"$inc": {"sequence_value": 1}},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            
            return result["sequence_value"]
            
        except Exception as e:
            # Method 2: Fallback to Beanie with retry logic
            print(f"MongoDB atomic operation failed, using fallback: {e}")
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    counter = await Counter.find_one(Counter.collection_name == "accounts")
                    
                    if not counter:
                        # Create new counter
                        counter = Counter(collection_name="accounts", sequence_value=1)
                        await counter.insert()
                        return 1
                    else:
                        # Increment existing counter
                        counter.sequence_value += 1
                        await counter.save()
                        return counter.sequence_value
                        
                except Exception as retry_error:
                    if attempt == max_retries - 1:
                        # Final fallback: use timestamp-based ID
                        import time
                        fallback_id = int(time.time()) % 100000
                        print(f"All methods failed, using timestamp fallback: {fallback_id}")
                        return fallback_id
                    
                    # Wait before retry
                    import asyncio
                    await asyncio.sleep(0.1)