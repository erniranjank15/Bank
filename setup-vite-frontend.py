#!/usr/bin/env python3
"""
Quick setup script for React Banking Frontend with Vite
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
    """Copy frontend files to the Vite React app"""
    print("📁 Copying frontend files...")
    
    frontend_files_dir = Path("frontend-files")
    target_dir = Path("bank-frontend")
    
    if not frontend_files_dir.exists():
        print("❌ frontend-files directory not found!")
        return False
    
    if not target_dir.exists():
        print("❌ bank-frontend directory not found! Please create Vite app first.")
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


def create_vite_config():
    """Create vite.config.js with proxy"""
    vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
"""
    
    try:
        with open("bank-frontend/vite.config.js", "w") as f:
            f.write(vite_config)
        print("✅ vite.config.js created with proxy")
        return True
    except Exception as e:
        print(f"❌ Error creating vite.config.js: {e}")
        return False


def create_env_file():
    """Create .env file"""
    env_content = """# React Banking App Environment Variables
VITE_API_URL=http://localhost:8000

# For production, change to your deployed API URL
# VITE_API_URL=https://your-api.onrender.com
"""
    
    try:
        with open("bank-frontend/.env", "w") as f:
            f.write(env_content)
        print("✅ .env file created")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def update_package_json():
    """Update package.json with additional scripts"""
    package_json_additions = """
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  }
}
"""
    print("✅ Package.json already configured by Vite")
    return True


def main():
    """Main setup process"""
    print("🏦 React Banking Frontend - Vite Setup")
    print("=" * 50)
    
    # Check if Node.js is installed
    if not run_command("node --version", "Checking Node.js"):
        print("❌ Node.js is not installed. Please install Node.js first.")
        return
    
    # Check if npm is installed
    if not run_command("npm --version", "Checking npm"):
        print("❌ npm is not installed. Please install npm first.")
        return
    
    # Create Vite React app if it doesn't exist
    if not os.path.exists("bank-frontend"):
        print("⚡ Creating Vite React app...")
        if not run_command("npm create vite@latest bank-frontend -- --template react", "Creating Vite React app"):
            return
    else:
        print("📦 Vite React app directory already exists")
    
    # Change to React app directory
    os.chdir("bank-frontend")
    
    # Install base dependencies
    if not run_command("npm install", "Installing base dependencies"):
        return
    
    # Install additional dependencies
    dependencies = [
        "axios",
        "react-router-dom", 
        "react-hook-form",
        "react-hot-toast",
        "lucide-react",
        "@headlessui/react"
    ]
    
    deps_string = " ".join(dependencies)
    if not run_command(f"npm install {deps_string}", "Installing additional dependencies"):
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
    
    # Create Vite config
    if not create_vite_config():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    print("\n" + "=" * 50)
    print("🎉 Vite React setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start your FastAPI backend:")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\n2. Start the Vite React frontend:")
    print("   cd bank-frontend")
    print("   npm run dev")
    print("\n3. Open your browser:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000/docs")
    print("\n🔐 Default login credentials:")
    print("   Admin: username=admin, password=admin123")
    print("   User:  username=john_doe, password=password123")
    print("\n⚡ Vite Benefits:")
    print("   - Much faster development server")
    print("   - Instant hot module replacement")
    print("   - Faster builds")
    print("   - Better development experience")


if __name__ == "__main__":
    main()