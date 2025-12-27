# Bank Management System - MongoDB Version

This project has been converted from SQLite to MongoDB with cloud connectivity support.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. MongoDB Setup

#### Option A: MongoDB Atlas (Cloud - Recommended)

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string from the "Connect" button
4. Update your `.env` file:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=bank_system
```

#### Option B: Local MongoDB

1. Install MongoDB locally
2. Update your `.env` file:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=bank_system
```

### 3. Initialize Database

```bash
python setup_mongodb.py
```

This will:
- Test your MongoDB connection
- Create necessary indexes
- Create a default admin user (username: `admin`, password: `admin123`)

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📊 Data Migration

If you have existing SQLite data, you can migrate it to MongoDB:

```bash
python migrate_sqlite_to_mongodb.py
```

**Note:** Make sure your `accounts.db` file is in the project directory before running the migration.

## 🔧 Key Changes from SQLite Version

### Database Layer
- **SQLAlchemy** → **Beanie ODM** (built on Pydantic and Motor)
- **SQLite** → **MongoDB**
- **Integer IDs** → **MongoDB ObjectIds**
- **Foreign Keys** → **Document References**

### Models
- `Users` and `Accounts` are now MongoDB documents
- Automatic `_id` field (ObjectId) instead of auto-increment integers
- Built-in validation with Pydantic
- Indexes defined in model classes

### Repository Layer
- All database operations are now `async`
- MongoDB-specific error handling
- Document-based queries instead of SQL

### API Changes
- All endpoints are now `async`
- ID parameters are strings (ObjectId format)
- Better error handling for invalid ObjectIds

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication

The JWT authentication system remains the same:

1. **POST** `/login` - Get access token
2. Use the token in the `Authorization` header: `Bearer <token>`

### Default Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `admin`

## 📋 API Endpoints

### Users
- `POST /users/` - Create user
- `GET /users/` - List all users (admin only)
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user (admin only)

### Accounts
- `POST /accounts/` - Create account
- `GET /accounts/` - List all accounts (admin only)
- `GET /accounts/{id}` - Get account details
- `PATCH /accounts/{id}` - Update account (user)
- `PUT /accounts/{id}/admin` - Update account (admin)
- `DELETE /accounts/{id}` - Delete account (admin)
- `POST /accounts/{id}/deposit` - Deposit funds
- `POST /accounts/{id}/withdraw` - Withdraw funds

## 🛠️ Development

### Project Structure
```
├── models.py              # MongoDB document models
├── database.py            # MongoDB connection and setup
├── schemas.py             # Pydantic schemas for API
├── auth.py                # JWT authentication
├── security.py            # Password hashing
├── main.py                # FastAPI application
├── repository/            # Data access layer
│   ├── accounts.py
│   └── users.py
├── routers/               # API route handlers
│   ├── accounts.py
│   └── users.py
├── setup_mongodb.py       # Database setup script
└── migrate_sqlite_to_mongodb.py  # Migration script
```

### Environment Variables
```env
# App Configuration
APP_NAME=Bank Management API
SECRET_KEY=BANK_SECRET_KEY_123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MongoDB Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=bank_system
```

## 🔍 Testing

You can test the API using:
- **Swagger UI**: `http://localhost:8000/docs`
- **Postman** or **Insomnia**
- **curl** commands

### Example: Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "mob_no": 1234567890,
    "hashed_password": "password123",
    "role": "user"
  }'
```

### Example: Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

## 🚨 Important Notes

1. **ObjectIds**: All IDs are now MongoDB ObjectIds (24-character hex strings)
2. **Async Operations**: All database operations are asynchronous
3. **Validation**: Enhanced data validation with Pydantic models
4. **Indexes**: Unique constraints are enforced via MongoDB indexes
5. **Relationships**: User-Account relationships are maintained via document references

## 🔧 Troubleshooting

### Connection Issues
- Verify your MongoDB connection string in `.env`
- Check if your IP is whitelisted in MongoDB Atlas
- Ensure your username/password are correct

### Migration Issues
- Make sure `accounts.db` exists before running migration
- Check for duplicate usernames/emails in your SQLite data

### Performance
- MongoDB indexes are automatically created for optimal performance
- Consider adding more indexes based on your query patterns

## 📈 Scaling

This MongoDB setup is ready for production and can handle:
- Horizontal scaling with MongoDB sharding
- High availability with replica sets
- Cloud deployment with MongoDB Atlas
- Advanced features like aggregation pipelines and full-text search

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.