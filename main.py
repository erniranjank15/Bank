from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
import os

from database import init_db
from routers import accounts as accounts_router
from routers import users as users_router
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import Token
from models import Users
from security import verify_password

app = FastAPI(
    title="Bank Management System API",
    description="A comprehensive banking system with MongoDB backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - secure for production
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    "https://banknk.netlify.app",  # Your deployed frontend (no trailing slash)
    # Add more domains if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Restrict to specific origins for security
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    await init_db()
    print("✅ Database initialized successfully")

# Include routers
app.include_router(accounts_router.router)
app.include_router(users_router.router)

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Bank Management System API!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user by username
    user = await Users.find_one(Users.username == form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.user_id,
            "role": user.role
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }