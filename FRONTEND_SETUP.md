# 🏦 React Banking Frontend - Setup Guide

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Your FastAPI backend running (on localhost:8000 or deployed)

## 🚀 Quick Setup

### Step 1: Create React App Directory
```bash
mkdir bank-frontend
cd bank-frontend
```

### Step 2: Initialize React App
```bash
npx create-react-app . --template typescript
# OR for JavaScript version:
npx create-react-app .
```

### Step 3: Install Dependencies
```bash
npm install axios react-router-dom react-hook-form react-hot-toast lucide-react @headlessui/react
```

### Step 4: Install Tailwind CSS
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 5: Copy Frontend Files
Copy all files from the `frontend-files/` directory to your `bank-frontend/` directory:

```
bank-frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.js
│   │   │   └── Register.js
│   │   ├── Profile/
│   │   │   ├── Profile.js
│   │   │   └── UserProfileCard.js
│   │   ├── Users/
│   │   │   └── UserList.js
│   │   ├── Accounts/
│   │   │   ├── AccountList.js
│   │   │   ├── AccountDetails.js
│   │   │   └── CreateAccount.js
│   │   ├── Transactions/
│   │   │   └── TransactionModal.js
│   │   ├── Layout/
│   │   │   └── Layout.js
│   │   └── UI/
│   │       └── LoadingSpinner.js
│   ├── context/
│   │   ├── AuthContext.js
│   │   └── BankContext.js
│   ├── App.js
│   └── index.css
├── tailwind.config.js
└── package.json
```

### Step 6: Update Configuration Files

**Update `tailwind.config.js`:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        banking: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        }
      },
    },
  },
  plugins: [],
}
```

**Update `package.json` (add proxy):**
```json
{
  "name": "bank-frontend",
  "version": "0.1.0",
  "private": true,
  "proxy": "http://localhost:8000",
  "dependencies": {
    // ... your dependencies
  }
}
```

### Step 7: Environment Variables
Create `.env` file in root:
```env
REACT_APP_API_URL=http://localhost:8000
# For production, change to your deployed API URL
# REACT_APP_API_URL=https://your-api.onrender.com
```

### Step 8: Start the App
```bash
npm start
```

## 🎯 **Running the Complete System**

### 1. Start Backend (FastAPI)
```bash
# In your backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend (React)
```bash
# In your bank-frontend directory
npm start
```

### 3. Access the App
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔐 **Default Login Credentials**

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test User:**
- Username: `john_doe`
- Password: `password123`

## 📱 **App Features**

### For Users:
- ✅ Login/Register
- ✅ View personal profile
- ✅ Manage bank accounts
- ✅ Deposit/Withdraw money
- ✅ View account details

### For Admins:
- ✅ All user features
- ✅ View all users
- ✅ Manage any account
- ✅ User profile details
- ✅ System overview

## 🛠️ **Troubleshooting**

### Common Issues:

1. **CORS Errors:**
   - Make sure backend has CORS enabled
   - Check if proxy is set in package.json

2. **API Connection:**
   - Verify backend is running on port 8000
   - Check REACT_APP_API_URL in .env

3. **Dependencies:**
   - Delete node_modules and run `npm install`
   - Check Node.js version (v16+)

4. **Tailwind Not Working:**
   - Verify tailwind.config.js content paths
   - Check if @tailwind directives are in index.css

### Development Commands:
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 🚀 **Production Deployment**

### Build for Production:
```bash
npm run build
```

### Deploy Options:
- **Netlify**: Drag & drop build folder
- **Vercel**: Connect GitHub repo
- **Render**: Static site deployment

### Environment Variables for Production:
```env
REACT_APP_API_URL=https://your-deployed-api.onrender.com
```

## 📖 **Next Steps**

1. Customize the UI colors and branding
2. Add more transaction features
3. Implement transaction history
4. Add user settings page
5. Create admin dashboard

Your banking app is now ready to run! 🎉