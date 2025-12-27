"""
Add sample data to test the database
"""

import asyncio
from database import init_db
from models import Users, Accounts
from security import get_password_hash


async def add_sample_data():
    """Add sample users and accounts"""
    print("🔧 Adding sample data...")
    
    # Initialize database
    await init_db()
    
    # Check if admin user already exists
    admin_user = await Users.find_one(Users.username == "admin")
    if not admin_user:
        # Create admin user
        admin_user = Users(
            username="admin",
            email="admin@bank.com",
            mob_no=1234567890,
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        await admin_user.insert()
        print("✅ Admin user created")
    else:
        print("ℹ️  Admin user already exists")
    
    # Check if test user exists
    test_user = await Users.find_one(Users.username == "john_doe")
    if not test_user:
        # Create test user
        test_user = Users(
            username="john_doe",
            email="john@example.com",
            mob_no=9876543210,
            hashed_password=get_password_hash("password123"),
            role="user"
        )
        await test_user.insert()
        print("✅ Test user created")
        
        # Create sample account for test user
        sample_account = Accounts(
            acc_holder_name="John Doe",
            acc_holder_address="123 Main Street, City",
            dob="1990-01-15",
            gender="Male",
            acc_type="Savings",
            balance=5000.0,
            ifsc_code=123456,
            branch="Main Branch",
            user_id=str(test_user.id)
        )
        await sample_account.insert()
        print("✅ Sample account created")
    else:
        print("ℹ️  Test user already exists")
    
    print("\n🎉 Sample data setup complete!")
    print("\n📋 Login credentials:")
    print("   Admin: username=admin, password=admin123")
    print("   User:  username=john_doe, password=password123")


if __name__ == "__main__":
    print("🏦 Bank System - Sample Data Setup")
    print("="*50)
    
    try:
        asyncio.run(add_sample_data())
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your MongoDB connection is working.")