# 👤 User Profile Endpoint Guide

## 🎯 New Profile Route Added

I've added a dedicated profile endpoint that allows logged-in users to view their complete profile information with all associated accounts.

## 📍 **Endpoint Details**

### **GET /users/profile**
- **Description**: Get current user's profile with all associated accounts and summary information
- **Authentication**: Required (JWT token)
- **Authorization**: Any authenticated user (user or admin)
- **Method**: GET
- **URL**: `http://localhost:8000/users/profile`

## 📋 **Response Schema**

```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "mob_no": 1234567890,
  "role": "user",
  "created_at": "2024-01-15T10:30:00",
  "accounts": [
    {
      "acc_no": 1,
      "acc_holder_name": "John Doe",
      "acc_holder_address": "123 Main St",
      "dob": "1990-01-01",
      "gender": "Male",
      "acc_type": "Savings",
      "balance": 1500.00,
      "ifsc_code": 123456,
      "branch": "Main Branch",
      "created_at": "2024-01-15T10:35:00",
      "user_id": 1
    }
  ],
  "total_balance": 1500.00,
  "total_accounts": 1
}
```

## 🔧 **Key Features**

### **1. Complete User Information**
- User ID (sequential: 1, 2, 3...)
- Username, email, mobile number
- Role (user/admin)
- Account creation date

### **2. Associated Accounts**
- All bank accounts belonging to the user
- Complete account details for each account
- Account numbers, balances, types, etc.

### **3. Summary Information**
- **Total Balance**: Sum of all account balances
- **Total Accounts**: Number of accounts owned

### **4. Security**
- Users can only see their own profile
- JWT token authentication required
- No sensitive data exposed (passwords hidden)

## 🚀 **How to Use**

### **1. Frontend Integration**
```javascript
// In your React app
const getMyProfile = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch('/users/profile', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const profile = await response.json();
  return profile;
};
```

### **2. cURL Testing**
```bash
# 1. Login first
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 2. Use the token from login response
curl -X GET "http://localhost:8000/users/profile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### **3. Python Testing**
```python
import requests

# Login
login_response = requests.post(
    "http://localhost:8000/login",
    data={"username": "admin", "password": "admin123"}
)
token = login_response.json()["access_token"]

# Get profile
profile_response = requests.get(
    "http://localhost:8000/users/profile",
    headers={"Authorization": f"Bearer {token}"}
)
profile = profile_response.json()
print(f"User: {profile['username']}")
print(f"Total Balance: ${profile['total_balance']}")
```

## 🔄 **Comparison with Other Endpoints**

| Endpoint | Purpose | Access | Data Returned |
|----------|---------|--------|---------------|
| `GET /users/profile` | **Current user's profile** | Own profile only | User + accounts + summary |
| `GET /users/{user_id}` | Specific user details | User or admin | User + accounts |
| `GET /users/` | All users list | Admin only | All users + accounts |

## 🎯 **Use Cases**

### **1. Profile Dashboard**
- Display user's complete profile information
- Show account summary (total balance, number of accounts)
- List all associated bank accounts

### **2. Account Overview**
- Quick view of all user's financial information
- Balance totals across all accounts
- Account management starting point

### **3. User Settings**
- Profile information for editing
- Account preferences
- Personal information management

## 🧪 **Testing the Endpoint**

### **Run the Test Script**
```bash
python test_profile_endpoint.py
```

### **Expected Output**
```
🧪 Testing Profile Endpoint
==================================================
1. Logging in...
✅ Login successful

2. Testing profile endpoint...
✅ Profile endpoint successful

📋 Profile Data:
   User ID: 1
   Username: admin
   Email: admin@bank.com
   Role: admin
   Total Accounts: 2
   Total Balance: $2500.00

💳 Associated Accounts (2):
   1. Account #1 - Savings - $1500.00
   2. Account #2 - Current - $1000.00
```

## 🔐 **Security Features**

### **1. Authentication Required**
- Must provide valid JWT token
- Token contains user identification

### **2. Authorization**
- Users can only access their own profile
- No way to access other users' profiles through this endpoint

### **3. Data Privacy**
- Password hash not included in response
- Only necessary profile information returned

## 📱 **Frontend Integration**

### **React Context Usage**
```javascript
// In your AuthContext or BankContext
const fetchUserProfile = async () => {
  try {
    const response = await axios.get('/users/profile');
    setUserProfile(response.data);
  } catch (error) {
    console.error('Failed to fetch profile:', error);
  }
};
```

### **Profile Component**
```javascript
const ProfilePage = () => {
  const [profile, setProfile] = useState(null);
  
  useEffect(() => {
    fetchUserProfile().then(setProfile);
  }, []);
  
  if (!profile) return <LoadingSpinner />;
  
  return (
    <div>
      <h1>Welcome, {profile.username}!</h1>
      <p>Total Balance: ${profile.total_balance}</p>
      <p>Accounts: {profile.total_accounts}</p>
      
      {profile.accounts.map(account => (
        <AccountCard key={account.acc_no} account={account} />
      ))}
    </div>
  );
};
```

## ✅ **Implementation Complete**

The profile endpoint is now fully implemented and ready to use:

- ✅ Route added: `GET /users/profile`
- ✅ Authentication and authorization implemented
- ✅ Repository function with summary calculations
- ✅ Response schema with profile data
- ✅ Test script for verification
- ✅ Documentation and examples

Your users can now access their complete profile information with all associated accounts through a single, secure endpoint!