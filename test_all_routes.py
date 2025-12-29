#!/usr/bin/env python3
"""
Comprehensive test script for all API routes
Tests both local and production environments
"""

import requests
import json
import time
from datetime import datetime

# Configuration
PRODUCTION_URL = "https://bank-4-yt2f.onrender.com"
LOCAL_URL = "http://localhost:8000"

# Test with production by default, change to LOCAL_URL for local testing
BASE_URL = PRODUCTION_URL

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.admin_token = None
        self.user_token = None
        self.test_user_id = None
        self.test_account_id = None
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }

    def log_result(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if details:
            print(f"      {details}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {details}")

    def test_basic_endpoints(self):
        """Test basic API endpoints"""
        print("\n🔍 Testing Basic Endpoints")
        print("=" * 50)

        # Test root endpoint
        try:
            response = requests.get(f"{self.base_url}/")
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Message: {data.get('message', 'N/A')}"
            self.log_result("GET /", success, details)
        except Exception as e:
            self.log_result("GET /", False, f"Error: {e}")

        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health")
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Status: {data.get('status', 'N/A')}"
            self.log_result("GET /health", success, details)
        except Exception as e:
            self.log_result("GET /health", False, f"Error: {e}")

        # Test API docs
        try:
            response = requests.get(f"{self.base_url}/docs")
            success = response.status_code == 200
            self.log_result("GET /docs", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("GET /docs", False, f"Error: {e}")

        # Test OpenAPI spec
        try:
            response = requests.get(f"{self.base_url}/openapi.json")
            success = response.status_code == 200
            self.log_result("GET /openapi.json", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("GET /openapi.json", False, f"Error: {e}")

    def test_authentication(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication")
        print("=" * 50)

        # Test admin login
        try:
            response = requests.post(
                f"{self.base_url}/login",
                data={"username": "admin", "password": "admin123"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                self.admin_token = data.get("access_token")
                details = f"Token received: {self.admin_token[:20]}..." if self.admin_token else "No token"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            self.log_result("POST /login (admin)", success, details)
        except Exception as e:
            self.log_result("POST /login (admin)", False, f"Error: {e}")

        # Test invalid login
        try:
            response = requests.post(
                f"{self.base_url}/login",
                data={"username": "invalid", "password": "wrong"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            success = response.status_code == 401
            details = f"Status: {response.status_code} (should be 401)"
            self.log_result("POST /login (invalid credentials)", success, details)
        except Exception as e:
            self.log_result("POST /login (invalid credentials)", False, f"Error: {e}")

    def test_user_routes(self):
        """Test user management routes"""
        print("\n👤 Testing User Routes")
        print("=" * 50)

        if not self.admin_token:
            print("   ⚠️  Skipping user tests - no admin token")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test profile endpoint
        try:
            response = requests.get(f"{self.base_url}/users/profile", headers=headers)
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Username: {data.get('username')}, Role: {data.get('role')}, Accounts: {data.get('total_accounts', 0)}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            self.log_result("GET /users/profile", success, details)
        except Exception as e:
            self.log_result("GET /users/profile", False, f"Error: {e}")

        # Test get all users (admin only)
        try:
            response = requests.get(f"{self.base_url}/users/", headers=headers)
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Found {len(data)} users"
            else:
                details = f"Status: {response.status_code}"
            self.log_result("GET /users/ (admin)", success, details)
        except Exception as e:
            self.log_result("GET /users/ (admin)", False, f"Error: {e}")

        # Test create user
        test_user_data = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "mob_no": int(f"9{int(time.time()) % 999999999}"),
            "hashed_password": "testpass123",
            "role": "user"
        }

        try:
            response = requests.post(
                f"{self.base_url}/users/",
                json=test_user_data,
                headers=headers
            )
            success = response.status_code == 201
            if success:
                data = response.json()
                self.test_user_id = data.get("user_id")
                details = f"Created user ID: {self.test_user_id}, Username: {data.get('username')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            self.log_result("POST /users/ (create user)", success, details)
        except Exception as e:
            self.log_result("POST /users/ (create user)", False, f"Error: {e}")

        # Test get specific user
        if self.test_user_id:
            try:
                response = requests.get(f"{self.base_url}/users/{self.test_user_id}", headers=headers)
                success = response.status_code == 200
                if success:
                    data = response.json()
                    details = f"User: {data.get('username')}, Accounts: {len(data.get('accounts', []))}"
                else:
                    details = f"Status: {response.status_code}"
                self.log_result(f"GET /users/{self.test_user_id}", success, details)
            except Exception as e:
                self.log_result(f"GET /users/{self.test_user_id}", False, f"Error: {e}")

    def test_account_routes(self):
        """Test account management routes"""
        print("\n💳 Testing Account Routes")
        print("=" * 50)

        if not self.admin_token:
            print("   ⚠️  Skipping account tests - no admin token")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test get all accounts (admin only)
        try:
            response = requests.get(f"{self.base_url}/accounts/", headers=headers)
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Found {len(data)} accounts"
                if data:
                    self.test_account_id = data[0].get("acc_no")
            else:
                details = f"Status: {response.status_code}"
            self.log_result("GET /accounts/ (admin)", success, details)
        except Exception as e:
            self.log_result("GET /accounts/ (admin)", False, f"Error: {e}")

        # Test create account
        if self.test_user_id:
            account_data = {
                "acc_holder_name": "Test Account Holder",
                "acc_holder_address": "123 Test Street",
                "dob": "1990-01-01",
                "gender": "Male",
                "acc_type": "Savings",
                "balance": 500.0,
                "ifsc_code": 123456,
                "branch": "Test Branch"
            }

            try:
                response = requests.post(
                    f"{self.base_url}/accounts/",
                    json=account_data,
                    headers=headers
                )
                success = response.status_code == 201
                if success:
                    data = response.json()
                    new_account_id = data.get("acc_no")
                    details = f"Created account ID: {new_account_id}, Balance: ${data.get('balance')}"
                    if not self.test_account_id:
                        self.test_account_id = new_account_id
                else:
                    details = f"Status: {response.status_code}, Response: {response.text}"
                self.log_result("POST /accounts/ (create account)", success, details)
            except Exception as e:
                self.log_result("POST /accounts/ (create account)", False, f"Error: {e}")

        # Test get specific account
        if self.test_account_id:
            try:
                response = requests.get(f"{self.base_url}/accounts/{self.test_account_id}", headers=headers)
                success = response.status_code == 200
                if success:
                    data = response.json()
                    details = f"Account: {data.get('acc_holder_name')}, Balance: ${data.get('balance')}"
                else:
                    details = f"Status: {response.status_code}"
                self.log_result(f"GET /accounts/{self.test_account_id}", success, details)
            except Exception as e:
                self.log_result(f"GET /accounts/{self.test_account_id}", False, f"Error: {e}")

    def test_transaction_routes(self):
        """Test deposit and withdraw routes"""
        print("\n💰 Testing Transaction Routes")
        print("=" * 50)

        if not self.admin_token or not self.test_account_id:
            print("   ⚠️  Skipping transaction tests - missing token or account ID")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Get initial balance
        initial_balance = 0
        try:
            response = requests.get(f"{self.base_url}/accounts/{self.test_account_id}", headers=headers)
            if response.status_code == 200:
                initial_balance = response.json().get("balance", 0)
        except:
            pass

        # Test deposit
        deposit_amount = 100.50
        try:
            response = requests.post(
                f"{self.base_url}/accounts/{self.test_account_id}/deposit?amount={deposit_amount}",
                headers=headers
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                new_balance = data.get("balance")
                expected_balance = initial_balance + deposit_amount
                balance_correct = abs(new_balance - expected_balance) < 0.01
                details = f"Deposited ${deposit_amount}, New balance: ${new_balance}, Expected: ${expected_balance}"
                if not balance_correct:
                    success = False
                    details += " (Balance mismatch!)"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            self.log_result(f"POST /accounts/{self.test_account_id}/deposit", success, details)
            
            if success:
                initial_balance = new_balance
        except Exception as e:
            self.log_result(f"POST /accounts/{self.test_account_id}/deposit", False, f"Error: {e}")

        # Test withdraw
        withdraw_amount = 50.25
        try:
            response = requests.post(
                f"{self.base_url}/accounts/{self.test_account_id}/withdraw?amount={withdraw_amount}",
                headers=headers
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                new_balance = data.get("balance")
                expected_balance = initial_balance - withdraw_amount
                balance_correct = abs(new_balance - expected_balance) < 0.01
                details = f"Withdrew ${withdraw_amount}, New balance: ${new_balance}, Expected: ${expected_balance}"
                if not balance_correct:
                    success = False
                    details += " (Balance mismatch!)"
            else:
                details = f"Status: {response.status_code}, Response: {response.text}"
            self.log_result(f"POST /accounts/{self.test_account_id}/withdraw", success, details)
        except Exception as e:
            self.log_result(f"POST /accounts/{self.test_account_id}/withdraw", False, f"Error: {e}")

        # Test insufficient funds
        try:
            large_amount = 999999.99
            response = requests.post(
                f"{self.base_url}/accounts/{self.test_account_id}/withdraw?amount={large_amount}",
                headers=headers
            )
            success = response.status_code == 400  # Should fail with insufficient funds
            details = f"Status: {response.status_code} (should be 400 for insufficient funds)"
            self.log_result("POST /withdraw (insufficient funds)", success, details)
        except Exception as e:
            self.log_result("POST /withdraw (insufficient funds)", False, f"Error: {e}")

    def test_error_cases(self):
        """Test error handling"""
        print("\n⚠️  Testing Error Cases")
        print("=" * 50)

        # Test unauthorized access
        try:
            response = requests.get(f"{self.base_url}/users/")
            success = response.status_code == 401
            details = f"Status: {response.status_code} (should be 401)"
            self.log_result("GET /users/ (no auth)", success, details)
        except Exception as e:
            self.log_result("GET /users/ (no auth)", False, f"Error: {e}")

        # Test invalid token
        try:
            headers = {"Authorization": "Bearer invalid_token"}
            response = requests.get(f"{self.base_url}/users/profile", headers=headers)
            success = response.status_code == 401
            details = f"Status: {response.status_code} (should be 401)"
            self.log_result("GET /users/profile (invalid token)", success, details)
        except Exception as e:
            self.log_result("GET /users/profile (invalid token)", False, f"Error: {e}")

        # Test non-existent resource
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"} if self.admin_token else {}
            response = requests.get(f"{self.base_url}/accounts/99999", headers=headers)
            success = response.status_code == 404
            details = f"Status: {response.status_code} (should be 404)"
            self.log_result("GET /accounts/99999 (not found)", success, details)
        except Exception as e:
            self.log_result("GET /accounts/99999 (not found)", False, f"Error: {e}")

    def cleanup_test_data(self):
        """Clean up test data"""
        print("\n🧹 Cleaning Up Test Data")
        print("=" * 50)

        if not self.admin_token or not self.test_user_id:
            print("   ℹ️  No cleanup needed")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Delete test user (this should cascade delete accounts)
        try:
            response = requests.delete(f"{self.base_url}/users/{self.test_user_id}", headers=headers)
            success = response.status_code in [200, 204]
            details = f"Status: {response.status_code}"
            self.log_result(f"DELETE /users/{self.test_user_id} (cleanup)", success, details)
        except Exception as e:
            self.log_result(f"DELETE /users/{self.test_user_id} (cleanup)", False, f"Error: {e}")

    def run_all_tests(self):
        """Run all tests"""
        print(f"🧪 Testing API: {self.base_url}")
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        self.test_basic_endpoints()
        self.test_authentication()
        self.test_user_routes()
        self.test_account_routes()
        self.test_transaction_routes()
        self.test_error_cases()
        self.cleanup_test_data()

        # Print summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📈 Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")

        if self.results['errors']:
            print(f"\n❌ Failed Tests:")
            for error in self.results['errors']:
                print(f"   • {error}")

        print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Overall status
        if self.results['failed'] == 0:
            print("\n🎉 ALL TESTS PASSED! Your API is working perfectly! 🎉")
        elif self.results['failed'] <= 2:
            print(f"\n⚠️  Minor issues found ({self.results['failed']} failures). API is mostly functional.")
        else:
            print(f"\n🚨 Multiple issues found ({self.results['failed']} failures). Please review the errors.")

def main():
    """Main function"""
    print("🏦 Bank Management System API - Comprehensive Route Testing")
    print("=" * 70)
    
    # Test production
    print(f"\n🌐 Testing Production API: {PRODUCTION_URL}")
    production_tester = APITester(PRODUCTION_URL)
    production_tester.run_all_tests()

if __name__ == "__main__":
    main()