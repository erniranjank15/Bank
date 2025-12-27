"""
Test script to verify auto-increment IDs work correctly
"""

import asyncio
from database import init_db
from models import Users, Accounts, Counter
from security import get_password_hash


async def test_auto_increment():
    """Test the auto-increment functionality"""
    print("🧪 Testing Auto-Increment IDs...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # Clear existing data for clean test
    await Users.delete_all()
    await Accounts.delete_all()
    await Counter.delete_all()
    print("🧹 Cleared existing data")
    
    print("\n" + "="*50)
    print("👥 Testing User Auto-Increment IDs")
    print("="*50)
    
    # Create 3 test users
    for i in range(1, 4):
        next_id = await Users.get_next_id()
        print(f"Next User ID: {next_id}")
        
        user = Users(
            user_id=next_id,
            username=f"user{i}",
            email=f"user{i}@test.com",
            mob_no=1000000000 + i,
            hashed_password=get_password_hash("password123"),
            role="user"
        )
        await user.insert()
        print(f"✅ Created user with ID: {user.user_id}")
    
    print("\n" + "="*50)
    print("🏦 Testing Account Auto-Increment IDs")
    print("="*50)
    
    # Create 3 test accounts
    for i in range(1, 4):
        next_id = await Accounts.get_next_id()
        print(f"Next Account ID: {next_id}")
        
        account = Accounts(
            acc_no=next_id,
            acc_holder_name=f"Account Holder {i}",
            acc_holder_address=f"Address {i}",
            dob="1990-01-01",
            gender="Male",
            acc_type="Savings",
            balance=1000.0 + i * 100,
            user_id=i  # Link to user
        )
        await account.insert()
        print(f"✅ Created account with ID: {account.acc_no}")
    
    print("\n" + "="*50)
    print("📊 Final Results")
    print("="*50)
    
    # Verify all users
    users = await Users.find_all().to_list()
    print(f"Users created: {len(users)}")
    for user in users:
        print(f"  User ID: {user.user_id}, Username: {user.username}")
    
    # Verify all accounts
    accounts = await Accounts.find_all().to_list()
    print(f"Accounts created: {len(accounts)}")
    for account in accounts:
        print(f"  Account ID: {account.acc_no}, Holder: {account.acc_holder_name}, Balance: {account.balance}")
    
    # Check counters
    user_counter = await Counter.find_one(Counter.collection_name == "users")
    account_counter = await Counter.find_one(Counter.collection_name == "accounts")
    
    print(f"\nCounter Values:")
    print(f"  Users counter: {user_counter.sequence_value if user_counter else 'Not found'}")
    print(f"  Accounts counter: {account_counter.sequence_value if account_counter else 'Not found'}")
    
    print("\n🎉 Auto-increment test completed!")
    
    # Test if IDs are truly sequential
    user_ids = [user.user_id for user in users]
    account_ids = [account.acc_no for account in accounts]
    
    expected_user_ids = [1, 2, 3]
    expected_account_ids = [1, 2, 3]
    
    if user_ids == expected_user_ids:
        print("✅ User IDs are sequential: [1, 2, 3]")
    else:
        print(f"❌ User IDs are NOT sequential. Got: {user_ids}")
    
    if account_ids == expected_account_ids:
        print("✅ Account IDs are sequential: [1, 2, 3]")
    else:
        print(f"❌ Account IDs are NOT sequential. Got: {account_ids}")


if __name__ == "__main__":
    print("🏦 Bank System - Auto-Increment ID Test")
    print("="*50)
    
    try:
        asyncio.run(test_auto_increment())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()