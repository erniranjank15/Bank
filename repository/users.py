from fastapi import HTTPException, status
from models import Accounts, Users
from schemas import CreateUser as User, ShowUser
from security import get_password_hash
from pymongo.errors import DuplicateKeyError


async def get_all_users():
    """Get all users with their accounts"""
    users = await Users.find_all().to_list()
    result = []
    
    for user in users:
        # Get accounts for this user
        accounts = await Accounts.find(Accounts.user_id == user.user_id).to_list()
        user_dict = user.dict()
        user_dict["accounts"] = [account.dict() for account in accounts]
        result.append(user_dict)
    
    return result


async def create_user_with_account(request: User):
    """Create a new user"""
    # Get next auto-increment ID
    next_id = await Users.get_next_id()
    
    new_user = Users(
        user_id=next_id,
        username=request.username,
        hashed_password=get_password_hash(request.hashed_password),
        email=request.email,
        mob_no=request.mob_no,
        role=request.role,
    )

    try:
        await new_user.insert()
        return new_user.dict()
    except DuplicateKeyError as e:
        if "username" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists"
            )
        elif "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        elif "mob_no" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this mobile number already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed due to duplicate data"
            )


async def get_user_by_id(user_id: int):
    """Get user by ID with their accounts"""
    user = await Users.find_one(Users.user_id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get accounts for this user
    accounts = await Accounts.find(Accounts.user_id == user.user_id).to_list()
    user_dict = user.dict()
    user_dict["accounts"] = [account.dict() for account in accounts]
    
    return user_dict


async def get_user_profile(user_id: int):
    """Get user profile with detailed account information - optimized for profile view"""
    user = await Users.find_one(Users.user_id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get accounts for this user with additional profile information
    accounts = await Accounts.find(Accounts.user_id == user.user_id).to_list()
    
    # Calculate total balance across all accounts
    total_balance = sum(account.balance for account in accounts)
    
    user_dict = user.dict()
    user_dict["accounts"] = [account.dict() for account in accounts]
    user_dict["total_balance"] = total_balance
    user_dict["total_accounts"] = len(accounts)
    
    return user_dict


async def delete_user(user_id: int):
    """Delete user and cascade delete their accounts"""
    user = await Users.find_one(Users.user_id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    # Delete all accounts for this user (cascade delete)
    await Accounts.find(Accounts.user_id == user.user_id).delete()
    
    # Delete the user
    await user.delete()
    return {"message": "User deleted successfully"}


async def update_user(user_id: int, request: User):
    """Update user details"""
    user = await Users.find_one(Users.user_id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    # Update user fields
    update_data = request.dict(exclude_unset=True)
    if "hashed_password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["hashed_password"])
    
    try:
        for field, value in update_data.items():
            if field != "user_id":  # Don't update the ID
                setattr(user, field, value)
        await user.save()
        
        return user.dict()
    except DuplicateKeyError as e:
        if "username" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        elif "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        elif "mob_no" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update failed due to duplicate data"
            )