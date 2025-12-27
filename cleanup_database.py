"""
Clean up database and prepare for auto-increment IDs
"""

import asyncio
from database import client, DATABASE_NAME


async def cleanup_database():
    """Drop all collections and start fresh"""
    print("🧹 Cleaning up database...")
    
    try:
        # Get database
        db = client[DATABASE_NAME]
        
        # List all collections
        collections = await db.list_collection_names()
        print(f"Found collections: {collections}")
        
        # Drop all collections
        for collection_name in collections:
            await db.drop_collection(collection_name)
            print(f"✅ Dropped collection: {collection_name}")
        
        print("🎉 Database cleanup completed!")
        print("Now you can run your app with fresh auto-increment IDs")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")


if __name__ == "__main__":
    print("🏦 Bank System - Database Cleanup")
    print("="*50)
    print("⚠️  This will delete ALL data in your database!")
    
    confirm = input("Are you sure you want to continue? (y/N): ")
    if confirm.lower() == 'y':
        asyncio.run(cleanup_database())
    else:
        print("Cleanup cancelled.")