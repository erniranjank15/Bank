#!/usr/bin/env python3
"""
Quick Start Script for Bank Management System (MongoDB Version)
"""

import asyncio
import sys
import subprocess
import os
from pathlib import Path


def check_requirements():
    """Check if requirements.txt exists and install dependencies"""
    if Path("requirements.txt").exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    return True


def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️  .env file not found!")
        print("📝 Creating .env file from template...")
        
        if Path(".env.example").exists():
            # Copy example to .env
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ .env file created from .env.example")
            print("🔧 Please update the MONGODB_URL in .env file with your MongoDB connection string")
            return False
        else:
            print("❌ .env.example not found. Please create .env file manually.")
            return False
    return True


async def setup_database():
    """Setup MongoDB database"""
    try:
        from setup_mongodb import setup_database as setup_db
        await setup_db()
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("Please check your MongoDB connection string in .env file")
        return False


def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")


async def main():
    """Main setup and start process"""
    print("🏦 Bank Management System - MongoDB Version")
    print("=" * 50)
    
    # Step 1: Check and install dependencies
    if not check_requirements():
        return
    
    # Step 2: Check .env file
    if not check_env_file():
        print("\n⚠️  Please update your .env file with MongoDB connection details and run this script again.")
        return
    
    # Step 3: Setup database
    print("\n🔧 Setting up MongoDB database...")
    if not await setup_database():
        return
    
    # Step 4: Start server
    print("\n" + "=" * 50)
    print("🎉 Setup completed! Starting the server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔐 Default admin login: username=admin, password=admin123")
    print("=" * 50)
    
    start_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"❌ Setup failed: {e}")