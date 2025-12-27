"""
SQLite to MongoDB Migration Script
This script helps migrate existing data from SQLite to MongoDB.
"""

import asyncio
import sqlite3
from datetime import datetime
from database import init_db
from models import Users, Accounts
from security import get_password_hash


async def migrate_data():
    """Migrate data from SQLite to MongoDB"""
    print("🔄 Starting migration from SQLite to MongoDB...")
    
    # Initialize MongoDB
    await init_db()
    
    # Connect to SQLite database
    try:
        sqlite_conn = sqlite3.connect('accounts.db')
        sqlite_conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = sqlite_conn.cursor()
        
        print("✅ Connected to SQLite database")
        
        # Migrate Users
        print("📤 Migrating users...")
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()
        
        user_id_mapping = {}  # Map old user_id to new ObjectId
        
        for user_row in users_data:
            # Check if user already exists
            existing_user = await Users.find_one(Users.username == user_row['username'])
            if existing_user:
                print(f"⚠️  User '{user_row['username']}' already exists, skipping...")
                user_id_mapping[user_row['user_id']] = existing_user.id
                continue
            
            # Create new user
            new_user = Users(
                username=user_row['username'],
                email=user_row['email'],
                mob_no=user_row['mob_no'],
                hashed_password=user_row['hashed_password'],  # Already hashed
                role=user_row['role'],
                created_at=datetime.fromisoformat(user_row['created_at'].replace('Z', '+00:00')) if user_row['created_at'] else datetime.utcnow()
            )
            
            try:
                await new_user.insert()
                user_id_mapping[user_row['user_id']] = new_user.id
                print(f"✅ Migrated user: {user_row['username']}")
            except Exception as e:
                print(f"❌ Failed to migrate user {user_row['username']}: {e}")
        
        # Migrate Accounts
        print("📤 Migrating accounts...")
        cursor.execute("SELECT * FROM accounts")
        accounts_data = cursor.fetchall()
        
        for account_row in accounts_data:
            # Get the corresponding MongoDB user ID
            old_user_id = account_row['user_id']
            if old_user_id not in user_id_mapping:
                print(f"⚠️  User ID {old_user_id} not found for account {account_row['acc_no']}, skipping...")
                continue
            
            new_user_id = user_id_mapping[old_user_id]
            
            # Create new account
            new_account = Accounts(
                acc_holder_name=account_row['acc_holder_name'],
                acc_holder_address=account_row['acc_holder_address'],
                dob=account_row['dob'],
                gender=account_row['gender'],
                acc_type=account_row['acc_type'],
                balance=account_row['balance'],
                ifsc_code=account_row['ifsc_code'],
                branch=account_row['branch'],
                user_id=new_user_id,
                created_at=datetime.fromisoformat(account_row['created_at'].replace('Z', '+00:00')) if account_row['created_at'] else datetime.utcnow()
            )
            
            try:
                await new_account.insert()
                print(f"✅ Migrated account: {account_row['acc_holder_name']} (Balance: {account_row['balance']})")
            except Exception as e:
                print(f"❌ Failed to migrate account {account_row['acc_no']}: {e}")
        
        sqlite_conn.close()
        print("🎉 Migration completed successfully!")
        
        # Print summary
        total_users = await Users.count()
        total_accounts = await Accounts.count()
        print(f"\n📊 Migration Summary:")
        print(f"   Users in MongoDB: {total_users}")
        print(f"   Accounts in MongoDB: {total_accounts}")
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        print("Make sure 'accounts.db' exists in the current directory")
    except Exception as e:
        print(f"❌ Migration error: {e}")


if __name__ == "__main__":
    print("🔄 SQLite to MongoDB Migration Tool")
    print("=" * 50)
    print("⚠️  Make sure to backup your data before running this migration!")
    print("⚠️  This script assumes 'accounts.db' exists in the current directory")
    
    confirm = input("\nDo you want to proceed with the migration? (y/N): ")
    if confirm.lower() == 'y':
        asyncio.run(migrate_data())
    else:
        print("Migration cancelled.")