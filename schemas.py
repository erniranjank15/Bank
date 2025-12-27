from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class CreateAccount(BaseModel):
    acc_holder_name: str
    acc_holder_address: str
    dob: str
    gender: str
    acc_type: str
    balance: float = 100.0
    ifsc_code: int = 123456
    branch: str = "Main Branch"


class ShowAccount(BaseModel):
    acc_no: int  # Sequential ID like 1, 2, 3...
    acc_holder_name: str
    acc_holder_address: str
    dob: str
    gender: str
    acc_type: str
    balance: float
    ifsc_code: int
    branch: str
    created_at: datetime
    user_id: int  # Sequential user ID


class UpdateAccountbyUser(BaseModel):
    acc_holder_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    acc_holder_address: Optional[str] = None       
    balance: Optional[float] = None


class UpdateAccountbyAdmin(BaseModel):
    acc_holder_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    acc_holder_address: Optional[str] = None       
    balance: Optional[float] = None
    acc_type: Optional[str] = None


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    mob_no: int
    hashed_password: str
    role: str = "user"


class ShowUser(BaseModel):
    user_id: int  # Sequential ID like 1, 2, 3...
    username: str
    email: EmailStr
    mob_no: int
    role: str 
    created_at: datetime
    accounts: List[ShowAccount] = []


class Token(BaseModel):
    access_token: str
    token_type: str