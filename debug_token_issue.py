#!/usr/bin/env python3
"""
Debug script to identify the token validation issue
"""

import requests
import jwt
import json
from datetime import datetime

# Your production API URL
BASE_URL = "https://bank-4-yt2f.onrender.com"

# The problematic token from your request
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInVzZXJfaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc2NjkzNTA0OX0.RjffzCWrvj3QhKwyn4szrjoOxn47M8PN3t6B6SyZ8sU"

def debug_token():
    """Debug the token validation issue"""
    print("🔍 Debugging Token Validation Issue")
    print("=" * 60)
    
    # Step 1: Decode token without verification to see contents
    print("1. Decoding token contents (no verification)...")
    try:
        # Decode without verification to see the payload
        unverified_payload = jwt.decode(TOKEN, options={"verify_signature": False})
        print("✅ Token payload:")
        print(f"   Subject (username): {unverified_payload.get('sub')}")
        print(f"   User ID: {unverified_payload.get('user_id')}")
        print(f"   Role: {unverified_payload.get('role')}")
        print(f"   Expiration: {unverified_payload.get('exp')}")
        
        # Convert expiration to readable date
        exp_timestamp = unverified_payload.get('exp')
        if exp_timestamp:
            exp_date = datetime.fromtimestamp(exp_timestamp)
            current_time = datetime.now()
            print(f"   Expires at: {exp_date}")
            print(f"   Current time: {current_time}")
            print(f"   Token expired: {current_time > exp_date}")
            
    except Exception as e:
        print(f"❌ Error decoding token: {e}")
        return
    
    # Step 2: Test with different SECRET_KEY values
    print(f"\n2. Testing token validation with different keys...")
    
    possible_keys = [
        "BANK_SECRET_KEY_123",
        "your-super-secret-key-change-in-production",
        None  # This will cause an error
    ]
    
    for i, key in enumerate(possible_keys, 1):
        if key is None:
            print(f"   {i}. Testing with None key: SKIP")
            continue
            
        print(f"   {i}. Testing with key: '{key}'")
        try:
            payload = jwt.decode(TOKEN, key, algorithms=["HS256"])
            print(f"      ✅ SUCCESS - Token valid with this key!")
            print(f"      Username: {payload.get('sub')}")
            break
        except jwt.ExpiredSignatureError:
            print(f"      ❌ Token expired")
        except jwt.InvalidSignatureError:
            print(f"      ❌ Invalid signature - wrong key")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    # Step 3: Get a fresh token and test
    print(f"\n3. Getting fresh token from production...")
    try:
        login_response = requests.post(
            f"{BASE_URL}/login",
            data={"username": "admin", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code == 200:
            fresh_token = login_response.json()["access_token"]
            print("✅ Got fresh token")
            print(f"   Token (first 20 chars): {fresh_token[:20]}...")
            
            # Test fresh token immediately
            print(f"\n4. Testing fresh token...")
            profile_response = requests.get(
                f"{BASE_URL}/users/profile",
                headers={"Authorization": f"Bearer {fresh_token}"}
            )
            
            print(f"   Profile request status: {profile_response.status_code}")
            if profile_response.status_code == 200:
                print("✅ Fresh token works!")
                profile = profile_response.json()
                print(f"   Username: {profile.get('username')}")
            else:
                print(f"❌ Fresh token also fails: {profile_response.text}")
                
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing fresh token: {e}")

def check_environment_variables():
    """Check what environment variables might be set"""
    print(f"\n" + "=" * 60)
    print("🔧 Environment Variable Analysis")
    print("Expected in production:")
    print("   SECRET_KEY=BANK_SECRET_KEY_123")
    print("   ALGORITHM=HS256")
    print("   ACCESS_TOKEN_EXPIRE_MINUTES=30")
    print("\nIf the fresh token test fails, the issue is likely:")
    print("   1. Environment variables not set correctly on Render")
    print("   2. App not redeployed after render.yaml changes")
    print("   3. Different SECRET_KEY used for creation vs validation")

if __name__ == "__main__":
    debug_token()
    check_environment_variables()
    
    print(f"\n" + "=" * 60)
    print("💡 Quick Fix Suggestions:")
    print("1. Redeploy your app on Render to ensure env vars are updated")
    print("2. Check Render dashboard for environment variable values")
    print("3. If fresh token works, the old token was created with different key")
    print("4. If fresh token fails, there's an environment configuration issue")