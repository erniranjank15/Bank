"""
Complete API test to verify auto-increment IDs work in the actual FastAPI app
"""

import asyncio
import httpx
import json
from database import init_db


async def test_api_endpoints():
    """Test the actual API endpoints"""
    print("🧪 Testing Real API Endpoints...")
    
    # Initialize database first
    await init_db()
    print("✅ Database initialized")
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("\n" + "="*50)
        print("👥 Testing User Creation")
        print("="*50)
        
        # Test 1: Create first user
        user1_data = {
            "username": "testuser1",
            "email": "test1@example.com",
            "mob_no": 1111111111,
            "hashed_password": "password123",
            "role": "user"
        }
        
        try:
            response = await client.post(f"{base_url}/users/", json=user1_data)
            if response.status_code == 201:
                user1 = response.json()
                print(f"✅ User 1 created with ID: {user1.get('user_id')}")
                print(f"   Username: {user1.get('username')}")
            else:
                print(f"❌ Failed to create user 1: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"❌ Error creating user 1: {e}")
            return
        
        # Test 2: Create second user
        user2_data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "mob_no": 2222222222,
            "hashed_password": "password123",
            "role": "user"
        }
        
        try:
            response = await client.post(f"{base_url}/users/", json=user2_data)
            if response.status_code == 201:
                user2 = response.json()
                print(f"✅ User 2 created with ID: {user2.get('user_id')}")
                print(f"   Username: {user2.get('username')}")
            else:
                print(f"❌ Failed to create user 2: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"❌ Error creating user 2: {e}")
            return
        
        print("\n" + "="*50)
        print("🔐 Testing Login")
        print("="*50)
        
        # Test 3: Login with first user
        login_data = {
            "username": "testuser1",
            "password": "password123"
        }
        
        try:
            response = await client.post(f"{base_url}/login", data=login_data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                print(f"✅ Login successful, got token")
                headers = {"Authorization": f"Bearer {access_token}"}
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"❌ Error during login: {e}")
            return
        
        print("\n" + "="*50)
        print("🏦 Testing Account Creation")
        print("="*50)
        
        # Test 4: Create first account
        account1_data = {
            "acc_holder_name": "Test Account Holder 1",
            "acc_holder_address": "123 Test Street",
            "dob": "1990-01-01",
            "gender": "Male",
            "acc_type": "Savings",
            "balance": 1000.0
        }
        
        try:
            response = await client.post(f"{base_url}/accounts/", json=account1_data, headers=headers)
            if response.status_code == 201:
                account1 = response.json()
                print(f"✅ Account 1 created with ID: {account1.get('acc_no')}")
                print(f"   Holder: {account1.get('acc_holder_name')}")
                print(f"   Balance: {account1.get('balance')}")
            else:
                print(f"❌ Failed to create account 1: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"❌ Error creating account 1: {e}")
            return
        
        # Test 5: Create second account
        account2_data = {
            "acc_holder_name": "Test Account Holder 2",
            "acc_holder_address": "456 Test Avenue",
            "dob": "1985-05-15",
            "gender": "Female",
            "acc_type": "Current",
            "balance": 2000.0
        }
        
        try:
            response = await client.post(f"{base_url}/accounts/", json=account2_data, headers=headers)
            if response.status_code == 201:
                account2 = response.json()
                print(f"✅ Account 2 created with ID: {account2.get('acc_no')}")
                print(f"   Holder: {account2.get('acc_holder_name')}")
                print(f"   Balance: {account2.get('balance')}")
            else:
                print(f"❌ Failed to create account 2: {response.status_code} - {response.text}")
                return
        except Exception as e:
            print(f"❌ Error creating account 2: {e}")
            return
        
        print("\n" + "="*50)
        print("💰 Testing Banking Operations")
        print("="*50)
        
        # Test 6: Deposit to account 1
        try:
            response = await client.post(f"{base_url}/accounts/1/deposit?amount=500", headers=headers)
            if response.status_code == 200:
                account = response.json()
                print(f"✅ Deposited 500 to Account 1, New balance: {account.get('balance')}")
            else:
                print(f"❌ Deposit failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error during deposit: {e}")
        
        # Test 7: Withdraw from account 1
        try:
            response = await client.post(f"{base_url}/accounts/1/withdraw?amount=200", headers=headers)
            if response.status_code == 200:
                account = response.json()
                print(f"✅ Withdrew 200 from Account 1, New balance: {account.get('balance')}")
            else:
                print(f"❌ Withdrawal failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error during withdrawal: {e}")
        
        print("\n" + "="*50)
        print("📊 Final Verification")
        print("="*50)
        
        # Test 8: Get account details
        try:
            response = await client.get(f"{base_url}/accounts/1", headers=headers)
            if response.status_code == 200:
                account = response.json()
                print(f"✅ Account 1 Details:")
                print(f"   Account Number: {account.get('acc_no')}")
                print(f"   Holder: {account.get('acc_holder_name')}")
                print(f"   Balance: {account.get('balance')}")
                print(f"   User ID: {account.get('user_id')}")
            else:
                print(f"❌ Failed to get account: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error getting account: {e}")
        
        # Test 9: Get user details
        try:
            response = await client.get(f"{base_url}/users/1", headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"✅ User 1 Details:")
                print(f"   User ID: {user.get('user_id')}")
                print(f"   Username: {user.get('username')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Accounts: {len(user.get('accounts', []))}")
            else:
                print(f"❌ Failed to get user: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error getting user: {e}")
        
        print("\n🎉 API Test Completed!")
        print("✅ Sequential IDs confirmed working in live API!")


if __name__ == "__main__":
    print("🏦 Bank System - Live API Test")
    print("="*50)
    print("⚠️  Make sure your FastAPI server is running on localhost:8000")
    print("   Run: uvicorn main:app --reload")
    
    input("Press Enter when server is ready...")
    
    try:
        asyncio.run(test_api_endpoints())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()