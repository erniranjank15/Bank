#!/usr/bin/env python3
"""
Test script for the new profile endpoint
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_profile_endpoint():
    """Test the profile endpoint"""
    print("🧪 Testing Profile Endpoint")
    print("=" * 50)
    
    # Step 1: Login to get token
    print("1. Logging in...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure FastAPI is running on port 8000")
        return
    
    # Step 2: Test profile endpoint
    print("\n2. Testing profile endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
        
        if response.status_code == 200:
            profile_data = response.json()
            print("✅ Profile endpoint successful")
            print("\n📋 Profile Data:")
            print(f"   User ID: {profile_data.get('user_id')}")
            print(f"   Username: {profile_data.get('username')}")
            print(f"   Email: {profile_data.get('email')}")
            print(f"   Role: {profile_data.get('role')}")
            print(f"   Total Accounts: {profile_data.get('total_accounts', 0)}")
            print(f"   Total Balance: ${profile_data.get('total_balance', 0):.2f}")
            
            accounts = profile_data.get('accounts', [])
            if accounts:
                print(f"\n💳 Associated Accounts ({len(accounts)}):")
                for i, account in enumerate(accounts, 1):
                    print(f"   {i}. Account #{account.get('acc_no')} - {account.get('acc_type')} - ${account.get('balance'):.2f}")
            else:
                print("\n💳 No accounts found")
                
        else:
            print(f"❌ Profile endpoint failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error testing profile endpoint: {e}")
    
    # Step 3: Test with regular user (if exists)
    print("\n3. Testing with regular user...")
    login_data_user = {
        "username": "john_doe",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data=login_data_user,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            user_token = response.json()["access_token"]
            print("✅ User login successful")
            
            # Test profile with user token
            user_headers = {"Authorization": f"Bearer {user_token}"}
            response = requests.get(f"{BASE_URL}/users/profile", headers=user_headers)
            
            if response.status_code == 200:
                user_profile = response.json()
                print("✅ User profile endpoint successful")
                print(f"   Username: {user_profile.get('username')}")
                print(f"   Total Accounts: {user_profile.get('total_accounts', 0)}")
                print(f"   Total Balance: ${user_profile.get('total_balance', 0):.2f}")
            else:
                print(f"❌ User profile failed: {response.status_code}")
        else:
            print("ℹ️  Regular user 'john_doe' not found (this is normal)")
            
    except Exception as e:
        print(f"ℹ️  Could not test with regular user: {e}")

if __name__ == "__main__":
    test_profile_endpoint()