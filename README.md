# 🏦 Bank Management System API

A full-featured **Banking System REST API** built with **FastAPI** and **MongoDB Atlas**, featuring JWT authentication, role-based access control, and complete banking operations.

## 🌐 Live Demo

- **API**: [https://bank-4-yt2f.onrender.com](https://bank-4-yt2f.onrender.com)
- **API Docs**: [https://bank-4-yt2f.onrender.com/docs](https://bank-4-yt2f.onrender.com/docs)
- **Frontend**: [https://banknk.netlify.app](https://banknk.netlify.app)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **MongoDB Atlas** | Cloud database |
| **Beanie ODM** | MongoDB object modeling |
| **Motor** | Async MongoDB driver |
| **JWT (python-jose)** | Authentication tokens |
| **Passlib + Bcrypt** | Password hashing |
| **Pydantic** | Data validation |
| **Uvicorn + Gunicorn** | ASGI server |
| **Render** | Backend deployment |
| **Netlify** | Frontend deployment |

---

## 📁 Project Structure

```
Bank/
├── main.py                  # FastAPI app entry point
├── database.py              # MongoDB connection setup
├── models.py                # Beanie ODM document models
├── schemas.py               # Pydantic request/response schemas
├── auth.py                  # JWT authentication logic
├── security.py              # Password hashing utilities
├── routers/
│   ├── users.py             # User management routes
│   └── accounts.py          # Account management routes
├── repository/
│   ├── users.py             # User database operations
│   └── accounts.py          # Account database operations
├── requirements.txt         # Python dependencies
├── Procfile                 # Render process configuration
├── render.yaml              # Render deployment configuration
├── runtime.txt              # Python version specification
└── .env.example             # Environment variables template
```

---

## 🚀 Features

### 🔐 Authentication
- JWT-based authentication
- Token expiry (30 minutes)
- Role-based access control (user / admin)
- Secure password hashing with bcrypt

### 👤 User Management
- User registration with unique username, email, mobile number
- Sequential auto-increment IDs (1, 2, 3...)
- Admin can view and manage all users
- Users can view and update their own profile
- Profile endpoint with account summary (total balance, total accounts)

### 💳 Account Management
- Create multiple bank accounts per user
- Account types (Savings, Current, etc.)
- Minimum balance validation (₹100)
- Admin can manage all accounts
- Users can manage their own accounts

### 💰 Banking Operations
- Deposit money to any account
- Withdraw money with balance validation
- Insufficient funds protection
- Real-time balance updates

---

## 📋 API Endpoints

### 🔍 General
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Welcome message | No |
| `GET` | `/health` | Health check | No |
| `GET` | `/docs` | Interactive API docs | No |

### 🔐 Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/login` | Login and get JWT token | No |

### 👤 Users
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/users/` | Register new user | No |
| `GET` | `/users/profile` | Get own profile with accounts | User/Admin |
| `GET` | `/users/` | Get all users | Admin only |
| `GET` | `/users/{user_id}` | Get specific user | User/Admin |
| `PUT` | `/users/{user_id}` | Update user | User/Admin |
| `DELETE` | `/users/{user_id}` | Delete user | Admin only |

### 💳 Accounts
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/accounts/` | Create account | User/Admin |
| `GET` | `/accounts/` | Get all accounts | Admin only |
| `GET` | `/accounts/{id}` | Get account details | User/Admin |
| `PATCH` | `/accounts/{id}` | Update account | User only |
| `PUT` | `/accounts/{id}/admin` | Update account (admin) | Admin only |
| `DELETE` | `/accounts/{id}` | Delete account | Admin only |
| `POST` | `/accounts/{id}/deposit` | Deposit money | User/Admin |
| `POST` | `/accounts/{id}/withdraw` | Withdraw money | User/Admin |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MongoDB Atlas account
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/erniranjank15/Bank.git
cd Bank
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=bank_system
SECRET_KEY=your-super-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the API
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔑 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `john_doe` | `password123` |

---

## 📡 API Usage Examples

### Login
```bash
curl -X POST "https://bank-4-yt2f.onrender.com/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Get Profile
```bash
curl -X GET "https://bank-4-yt2f.onrender.com/users/profile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create User
```bash
curl -X POST "https://bank-4-yt2f.onrender.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "mob_no": 1234567890,
    "hashed_password": "password123",
    "role": "user"
  }'
```

### Create Account
```bash
curl -X POST "https://bank-4-yt2f.onrender.com/accounts/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "acc_holder_name": "John Doe",
    "acc_holder_address": "123 Main St",
    "dob": "1990-01-01",
    "gender": "Male",
    "acc_type": "Savings",
    "balance": 500.0
  }'
```

### Deposit Money
```bash
curl -X POST "https://bank-4-yt2f.onrender.com/accounts/1/deposit?amount=100" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Withdraw Money
```bash
curl -X POST "https://bank-4-yt2f.onrender.com/accounts/1/withdraw?amount=50" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🌐 JavaScript Fetch Examples

### Login
```javascript
const login = async (username, password) => {
  const response = await fetch("https://bank-4-yt2f.onrender.com/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${username}&password=${password}`
  });
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};
```

### Get Profile
```javascript
const getProfile = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch("https://bank-4-yt2f.onrender.com/users/profile", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  return await response.json();
};
```

### Deposit
```javascript
const deposit = async (accountId, amount) => {
  const token = localStorage.getItem('token');
  const response = await fetch(
    `https://bank-4-yt2f.onrender.com/accounts/${accountId}/deposit?amount=${amount}`,
    {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    }
  );
  return await response.json();
};
```

---

## 🚀 Deployment on Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### 2. Configure Render
Set these environment variables in Render dashboard:

| Variable | Value |
|----------|-------|
| `MONGODB_URL` | Your MongoDB Atlas connection string |
| `DATABASE_NAME` | `bank_system` |
| `SECRET_KEY` | Your secret key |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

### 3. Deploy
- Render auto-deploys on every push to `main`
- Or manually trigger from Render dashboard

---

## 🗄️ Database Schema

### Users Collection
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "mob_no": 1234567890,
  "hashed_password": "<bcrypt_hash>",
  "role": "user",
  "created_at": "2024-01-15T10:30:00"
}
```

### Accounts Collection
```json
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
  "user_id": 1,
  "created_at": "2024-01-15T10:35:00"
}
```

---

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Bcrypt Password Hashing** - Industry-standard password security
- **Role-Based Access Control** - User and Admin roles
- **CORS Protection** - Restricted to allowed origins
- **Environment Variables** - Sensitive data in env vars
- **Input Validation** - Pydantic schema validation

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Niranjan Kasote**
- GitHub: [@erniranjank15](https://github.com/erniranjank15)
- Repository: [erniranjank15/Bank](https://github.com/erniranjank15/Bank)

---

## 📞 Support

If you encounter any issues, please open an issue on GitHub or check the API documentation at [https://bank-4-yt2f.onrender.com/docs](https://bank-4-yt2f.onrender.com/docs).
