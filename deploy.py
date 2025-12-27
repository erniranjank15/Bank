#!/usr/bin/env python3
"""
Quick deployment preparation script
"""

import os
import subprocess
import sys


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None


def check_files():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "requirements.txt", 
        "render.yaml",
        "Procfile",
        "runtime.txt",
        "models.py",
        "database.py",
        "auth.py",
        "schemas.py",
        "security.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True


def main():
    """Main deployment preparation"""
    print("🚀 Bank Management API - Deployment Preparation")
    print("=" * 60)
    
    # Check if all files exist
    if not check_files():
        print("Please ensure all required files are present before deploying.")
        return
    
    # Check if git is initialized
    if not os.path.exists(".git"):
        print("📁 Initializing Git repository...")
        run_command("git init", "Git initialization")
        run_command("git branch -M main", "Setting main branch")
    
    # Add all files
    run_command("git add .", "Adding files to git")
    
    # Commit changes
    commit_message = input("Enter commit message (or press Enter for default): ").strip()
    if not commit_message:
        commit_message = "Prepare for Render deployment"
    
    run_command(f'git commit -m "{commit_message}"', "Committing changes")
    
    print("\n" + "=" * 60)
    print("🎉 Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Push to GitHub: git push origin main")
    print("2. Go to https://dashboard.render.com")
    print("3. Create new Web Service")
    print("4. Connect your GitHub repository")
    print("5. Set environment variables:")
    print("   - MONGODB_URL (your MongoDB Atlas connection)")
    print("   - DATABASE_NAME=bank_system")
    print("   - SECRET_KEY=BANK_SECRET_KEY_123_PRODUCTION")
    print("6. Deploy!")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")


if __name__ == "__main__":
    main()