from datetime import datetime, timedelta
from jose import jwt, JWTError
from database import get_database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# Use environment variable for production security
SECRET_KEY = os.getenv("SECRET_KEY", "BANK_SECRET_KEY_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Validate SECRET_KEY is not None or empty
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set and not empty")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        role: str = payload.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "username": username,
            "user_id": user_id,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid"
        )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        role = payload.get("role")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        # Return user info without database lookup for performance
        return {
            "username": username,
            "user_id": int(user_id),
            "role": role
        }
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


async def admin_only(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Admin access required"
        )
    return current_user


async def user_or_admin(current_user=Depends(get_current_user)):
    if current_user["role"] not in ["user", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return current_user


async def user_only(current_user=Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=403, 
            detail="User access required"
        )
    return current_user