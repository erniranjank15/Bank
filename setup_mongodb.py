"""
MongoDB Setup Script
This script helps set up the MongoDB database and create initial indexes.
"""

import asyncio
from database import init_db, client, DATABASE_NAME
from models import Users, Accounts
from security import get_password_hash


async def setup_database():
    """Initialize MongoDB database and create indexes"""
    print("🚀 Setting up MongoDB database...")
    
    # Initialize Beanie ODM
    await init_db()
    print("✅ Database initialized with Beanie ODM")
    
    # Create indexes
    await Users.create_indexes()
    await Accounts.create_indexes()
    print("✅ Database indexes created")
    
    # Create a default admin user if it doesn't exist
    admin_user = await Users.find_one(Users.username == "admin")
    if not admin_user:
        admin_user = Users(
            username="admin",
            email="admin@bank.com",
            mob_no=1234567890,
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        await admin_user.insert()
        print("✅ Default admin user created (username: admin, password: admin123)")
    else:
        print("ℹ️  Admin user already exists")
    
    print("🎉 MongoDB setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with your MongoDB connection string")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: uvicorn main:app --reload")


async def test_connection():
    """Test MongoDB connection"""
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"📊 Available databases: {db_list}")
        
        if DATABASE_NAME in db_list:
            print(f"✅ Database '{DATABASE_NAME}' exists")
        else:
            print(f"ℹ️  Database '{DATABASE_NAME}' will be created on first write")
            
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("Please check your MONGODB_URL in the .env file")


if __name__ == "__main__":
    print("🔧 MongoDB Connection Test & Setup")
    print("=" * 50)
    
    # Test connection first
    asyncio.run(test_connection())
    
    print("\n" + "=" * 50)
    
    # Setup database
    asyncio.run(setup_database())