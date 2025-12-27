# 🚀 Render Deployment Guide

## Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **MongoDB Atlas**: Your MongoDB connection string
3. **Render Account**: Sign up at [render.com](https://render.com)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure these files are in your repository:
- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `Procfile` - Process file
- `runtime.txt` - Python version

### 2. Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 3. Deploy on Render

1. **Go to Render Dashboard**:
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Web Service"

2. **Connect Repository**:
   - Connect your GitHub account
   - Select your repository
   - Click "Connect"

3. **Configure Service**:
   - **Name**: `bank-management-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:
   Click "Advanced" → "Add Environment Variable":
   
   ```
   MONGODB_URL = mongodb+srv://kasoteniranjan23_db_user:Niranjan23@cluster0.mejihk9.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME = bank_system
   SECRET_KEY = BANK_SECRET_KEY_123_PRODUCTION
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

### 4. Test Your Deployment

Once deployed, you'll get a URL like: `https://bank-management-api.onrender.com`

Test endpoints:
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /docs` - API documentation

### 5. Create Initial Admin User

Use the API documentation at `https://your-app.onrender.com/docs`:

1. **Create Admin User**:
   ```json
   POST /users/
   {
     "username": "admin",
     "email": "admin@bank.com",
     "mob_no": 1234567890,
     "hashed_password": "admin123",
     "role": "admin"
   }
   ```

2. **Login**:
   ```
   POST /login
   username: admin
   password: admin123
   ```

## 🔧 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check `requirements.txt` format
   - Ensure Python version compatibility

2. **Database Connection Error**:
   - Verify MongoDB Atlas connection string
   - Check IP whitelist (allow 0.0.0.0/0 for Render)

3. **Environment Variables**:
   - Ensure all required variables are set
   - No quotes around values in Render dashboard

### Logs:
- Check deployment logs in Render dashboard
- Use "Events" tab for real-time logs

## 📱 API Usage

### Base URL:
```
https://your-app-name.onrender.com
```

### Key Endpoints:
- `POST /users/` - Create user
- `POST /login` - Login
- `POST /accounts/` - Create account
- `GET /accounts/{id}` - Get account
- `POST /accounts/{id}/deposit` - Deposit
- `POST /accounts/{id}/withdraw` - Withdraw

### Authentication:
All protected endpoints require:
```
Authorization: Bearer <your-jwt-token>
```

## 🎉 Success!

Your banking API is now live and accessible worldwide!

- **API Docs**: `https://your-app.onrender.com/docs`
- **Health Check**: `https://your-app.onrender.com/health`
- **Base URL**: `https://your-app.onrender.com`