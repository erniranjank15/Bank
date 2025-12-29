"""
Script to create React frontend for Banking API
"""

import os
import subprocess
import sys


def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_react_app():
    """Create React app with all dependencies"""
    print("🏦 Creating React Banking Frontend")
    print("=" * 50)
    
    # Create React app
    if not run_command("npx create-react-app bank-frontend", "Creating React app"):
        return False
    
    # Change to project directory
    os.chdir("bank-frontend")
    
    # Install additional dependencies
    dependencies = [
        "axios",           # HTTP client
        "react-router-dom", # Routing
        "react-hook-form", # Form handling
        "react-hot-toast", # Notifications
        "lucide-react",    # Icons
        "@headlessui/react", # UI components
    ]
    
    for dep in dependencies:
        if not run_command(f"npm install {dep}", f"Installing {dep}"):
            return False
    
    # Install Tailwind CSS
    if not run_command("npm install -D tailwindcss postcss autoprefixer", "Installing Tailwind CSS"):
        return False
    
    if not run_command("npx tailwindcss init -p", "Initializing Tailwind CSS"):
        return False
    
    print("🎉 React app created successfully!")
    print("📁 Project created in: bank-frontend/")
    return True


if __name__ == "__main__":
    create_react_app()