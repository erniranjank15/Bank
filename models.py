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
        """Get next auto-increment ID"""
        counter = await Counter.find_one(Counter.collection_name == "users")
        if not counter:
            counter = Counter(collection_name="users", sequence_value=1)
            await counter.insert()
            return 1
        else:
            counter.sequence_value += 1
            await counter.save()
            return counter.sequence_value


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
        """Get next auto-increment ID"""
        counter = await Counter.find_one(Counter.collection_name == "accounts")
        if not counter:
            counter = Counter(collection_name="accounts", sequence_value=1)
            await counter.insert()
            return 1
        else:
            counter.sequence_value += 1
            await counter.save()
            return counter.sequence_value