"""
Simple script to view MongoDB data
"""

import asyncio
from database import init_db
from models import Users, Accounts


async def view_all_data():
    """View all data in the database"""
    print("🔍 Connecting to MongoDB...")
    
    # Initialize database
    await init_db()
    print("✅ Connected to MongoDB!")
    
    print("\n" + "="*50)
    print("👥 USERS DATA")
    print("="*50)
    
    users = await Users.find_all().to_list()
    if users:
        for i, user in enumerate(users, 1):
            print(f"\n{i}. User ID: {user.id}")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Mobile: {user.mob_no}")
            print(f"   Role: {user.role}")
            print(f"   Created: {user.created_at}")
    else:
        print("No users found.")
    
    print("\n" + "="*50)
    print("🏦 ACCOUNTS DATA")
    print("="*50)
    
    accounts = await Accounts.find_all().to_list()
    if accounts:
        for i, account in enumerate(accounts, 1):
            print(f"\n{i}. Account ID: {account.id}")
            print(f"   Holder: {account.acc_holder_name}")
            print(f"   Address: {account.acc_holder_address}")
            print(f"   DOB: {account.dob}")
            print(f"   Gender: {account.gender}")
            print(f"   Type: {account.acc_type}")
            print(f"   Balance: ₹{account.balance}")
            print(f"   IFSC: {account.ifsc_code}")
            print(f"   Branch: {account.branch}")
            print(f"   User ID: {account.user_id}")
            print(f"   Created: {account.created_at}")
    else:
        print("No accounts found.")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Users: {len(users)}")
    print(f"   Total Accounts: {len(accounts)}")


async def view_users_with_accounts():
    """View users with their accounts"""
    print("\n" + "="*50)
    print("👥 USERS WITH THEIR ACCOUNTS")
    print("="*50)
    
    users = await Users.find_all().to_list()
    
    for user in users:
        print(f"\n👤 {user.username} ({user.email})")
        print(f"   Role: {user.role}")
        
        # Find accounts for this user
        user_accounts = await Accounts.find(Accounts.user_id == str(user.id)).to_list()
        
        if user_accounts:
            print(f"   Accounts ({len(user_accounts)}):")
            for account in user_accounts:
                print(f"   🏦 {account.acc_holder_name} - Balance: ₹{account.balance}")
        else:
            print("   No accounts found.")


if __name__ == "__main__":
    print("🏦 Bank System - Data Viewer")
    print("="*50)
    
    try:
        # View all data
        asyncio.run(view_all_data())
        
        # View users with accounts
        asyncio.run(view_users_with_accounts())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your MongoDB connection is working.")