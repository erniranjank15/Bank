#!/usr/bin/env python3
"""
Quick setup script for React Banking Frontend
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path


def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def copy_files():
    """Copy frontend files to the React app"""
    print("📁 Copying frontend files...")
    
    frontend_files_dir = Path("frontend-files")
    target_dir = Path("bank-frontend")
    
    if not frontend_files_dir.exists():
        print("❌ frontend-files directory not found!")
        return False
    
    if not target_dir.exists():
        print("❌ bank-frontend directory not found! Please create React app first.")
        return False
    
    try:
        # Copy all files from frontend-files to bank-frontend
        for item in frontend_files_dir.rglob("*"):
            if item.is_file():
                # Calculate relative path
                rel_path = item.relative_to(frontend_files_dir)
                target_path = target_dir / rel_path
                
                # Create parent directories if they don't exist
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(item, target_path)
                print(f"   Copied: {rel_path}")
        
        print("✅ All files copied successfully!")
        return True
    except Exception as e:
        print(f"❌ Error copying files: {e}")
        return False


def create_env_file():
    """Create .env file"""
    env_content = """# React Banking App Environment Variables
REACT_APP_API_URL=http://localhost:8000

# For production, change to your deployed API URL
# REACT_APP_API_URL=https://your-api.onrender.com
"""
    
    try:
        with open("bank-frontend/.env", "w") as f:
            f.write(env_content)
        print("✅ .env file created")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def main():
    """Main setup process"""
    print("🏦 React Banking Frontend - Quick Setup")
    print("=" * 50)
    
    # Check if Node.js is installed
    if not run_command("node --version", "Checking Node.js"):
        print("❌ Node.js is not installed. Please install Node.js first.")
        return
    
    # Check if npm is installed
    if not run_command("npm --version", "Checking npm"):
        print("❌ npm is not installed. Please install npm first.")
        return
    
    # Create React app if it doesn't exist
    if not os.path.exists("bank-frontend"):
        print("📦 Creating React app...")
        if not run_command("npx create-react-app bank-frontend", "Creating React app"):
            return
    else:
        print("📦 React app directory already exists")
    
    # Change to React app directory
    os.chdir("bank-frontend")
    
    # Install dependencies
    dependencies = [
        "axios",
        "react-router-dom", 
        "react-hook-form",
        "react-hot-toast",
        "lucide-react",
        "@headlessui/react"
    ]
    
    for dep in dependencies:
        if not run_command(f"npm install {dep}", f"Installing {dep}"):
            return
    
    # Install Tailwind CSS
    if not run_command("npm install -D tailwindcss postcss autoprefixer", "Installing Tailwind CSS"):
        return
    
    if not run_command("npx tailwindcss init -p", "Initializing Tailwind CSS"):
        return
    
    # Go back to parent directory
    os.chdir("..")
    
    # Copy frontend files
    if not copy_files():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start your FastAPI backend:")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\n2. Start the React frontend:")
    print("   cd bank-frontend")
    print("   npm start")
    print("\n3. Open your browser:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000/docs")
    print("\n🔐 Default login credentials:")
    print("   Admin: username=admin, password=admin123")
    print("   User:  username=john_doe, password=password123")


if __name__ == "__main__":
    main()