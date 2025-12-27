from fastapi import HTTPException, status
from models import Accounts, Users
from schemas import CreateAccount, UpdateAccountbyUser as UpdateAccount, UpdateAccountbyAdmin
from pymongo.errors import DuplicateKeyError


async def get_all():
    """Get all accounts"""
    accounts = await Accounts.find_all().to_list()
    return [account.dict() for account in accounts]


async def create(request: CreateAccount, current_user):
    """Create a new account"""
    if request.balance < 100.0:
        raise HTTPException(
            status_code=400,
            detail="Initial balance must be at least 100"
        )
    
    # Verify user exists
    user = await Users.find_one(Users.user_id == current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get next auto-increment ID
    next_id = await Accounts.get_next_id()
    
    new_account = Accounts(
        acc_no=next_id,
        acc_holder_name=request.acc_holder_name,
        acc_holder_address=request.acc_holder_address,
        dob=request.dob,
        gender=request.gender,
        acc_type=request.acc_type,
        balance=request.balance,
        ifsc_code=request.ifsc_code,
        branch=request.branch,
        user_id=user.user_id
    )
    
    try:
        await new_account.insert()
        return new_account.dict()
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Account creation failed")


async def destroy(id: int):
    """Delete an account"""
    account = await Accounts.find_one(Accounts.acc_no == id)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id {id} not found")
    
    await account.delete()
    return {"message": "Account deleted successfully"}


async def update(id: int, request: UpdateAccount):
    """Update account (user level)"""
    account = await Accounts.find_one(Accounts.acc_no == id)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            if field != "acc_no":  # Don't update the ID
                setattr(account, field, value)
        await account.save()

    return account.dict()


async def admin_update(id: int, request: UpdateAccountbyAdmin):
    """Update account (admin level)"""
    account = await Accounts.find_one(Accounts.acc_no == id)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id {id} not found")

    update_data = request.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            if field != "acc_no":  # Don't update the ID
                setattr(account, field, value)
        await account.save()
        
    return account.dict()


async def show(id: int):
    """Get single account"""
    account = await Accounts.find_one(Accounts.acc_no == id)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id {id} not found")
    
    return account.dict()


async def deposit(id: int, amount: float):
    """Deposit money to account"""
    account = await Accounts.find_one(Accounts.acc_no == id)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id {id} not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    account.balance += amount
    await account.save()
    
    return account.dict()


async def withdraw(id: int, amount: float):
    """Withdraw money from account"""
    account = await Accounts.find_one(Accounts.acc_no == id)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id {id} not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")
        
    if amount > account.balance:
        raise HTTPException(status_code=400, detail="Insufficient funds for withdrawal")

    account.balance -= amount
    await account.save()
    
    return account.dict()