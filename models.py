from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime
from pymongo import IndexModel


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
        """Get next auto-increment ID - simplified and reliable"""
        try:
            # Simple approach: find the highest existing ID and add 1
            last_user = await cls.find().sort([("user_id", -1)]).limit(1).to_list()
            
            if last_user:
                return last_user[0].user_id + 1
            else:
                return 1
                
        except Exception as e:
            # If all else fails, use timestamp-based ID
            import time
            fallback_id = int(str(int(time.time()))[-6:])  # Last 6 digits of timestamp
            print(f"Using timestamp fallback ID: {fallback_id}")
            return fallback_id


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
        """Get next auto-increment ID - simplified and reliable"""
        try:
            # Simple approach: find the highest existing ID and add 1
            last_account = await cls.find().sort([("acc_no", -1)]).limit(1).to_list()
            
            if last_account:
                return last_account[0].acc_no + 1
            else:
                return 1
                
        except Exception as e:
            # If all else fails, use timestamp-based ID
            import time
            fallback_id = int(str(int(time.time()))[-6:])  # Last 6 digits of timestamp
            print(f"Using timestamp fallback ID: {fallback_id}")
            return fallback_id