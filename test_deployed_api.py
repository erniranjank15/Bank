#!/usr/bin/env python3
"""
Test script for deployed API on Render
"""

import requests
import json

# Replace with your actual Render URL
BASE_URL = "https://your-app-name.onrender.com"  # Update this!

def test_deployed_api():
    """Test the deployed API authentication"""
    print("🌐 Testing Deployed API Authentication")
    print("=" * 50)
    
    # Step 1: Test login
    print("1. Testing login...")
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
        
        print(f"   Login Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("✅ Login successful")
            print(f"   Token (first 20 chars): {token[:20]}...")
            
            # Step 2: Test profile with token
            print("\n2. Testing profile with token...")
            headers = {"Authorization": f"Bearer {token}"}
            
            profile_response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
            print(f"   Profile Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print("✅ Profile request successful")
                print(f"   Username: {profile.get('username')}")
                print(f"   User ID: {profile.get('user_id')}")
                print(f"   Role: {profile.get('role')}")
            elif profile_response.status_code == 401:
                print("❌ Profile request failed - 401 Unauthorized")
                print(f"   Response: {profile_response.text}")
                print("\n🔍 Possible issues:")
                print("   - SECRET_KEY mismatch between login and profile validation")
                print("   - Token format issue")
                print("   - Environment variable not set correctly")
            else:
                print(f"❌ Profile request failed - {profile_response.status_code}")
                print(f"   Response: {profile_response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("   Make sure to update BASE_URL with your actual Render URL")

def test_token_manually():
    """Manual token testing"""
    print(f"\n" + "=" * 50)
    print("🔧 Manual Testing Instructions:")
    print(f"1. Update BASE_URL in this script to your actual Render URL")
    print(f"2. Test login manually:")
    print(f'   curl -X POST "{BASE_URL}/login" \\')
    print(f'     -H "Content-Type: application/x-www-form-urlencoded" \\')
    print(f'     -d "username=admin&password=admin123"')
    print(f"\n3. Copy the access_token from the response")
    print(f"4. Test profile with the token:")
    print(f'   curl -X GET "{BASE_URL}/users/profile" \\')
    print(f'     -H "Authorization: Bearer YOUR_TOKEN_HERE"')

if __name__ == "__main__":
    test_deployed_api()
    test_token_manually()