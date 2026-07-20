from fastapi import HTTPException, status
from models import Accounts, Users
from schemas import CreateAccount, UpdateAccountbyUser as UpdateAccount, UpdateAccountbyAdmin
from pymongo.errors import DuplicateKeyError
from fastapi import BackgroundTasks
from service.emailService import send_email

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


async def deposit(id: int, amount: float, background_tasks: BackgroundTasks):
    """Deposit money to account and send email notification"""

    # Find account
    account = await Accounts.find_one(Accounts.acc_no == id)

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with id {id} not found"
        )

    # Validate amount
    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Deposit amount must be positive"
        )

    # Get linked user (email is stored here)
    user = await Users.find_one(Users.user_id == account.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Linked user not found"
        )

    # Store previous balance
    previous_balance = account.balance

    # Update balance
    account.balance += amount
    new_balance = account.balance

    # Save account
    await account.save()

    # ---------------- EMAIL TEMPLATE ----------------
    email_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">

        <h2 style="color: #16a34a;">Deposit Successful</h2>

        <p>Dear <b>{account.acc_holder_name}</b>,</p>

        <p>Your account has been credited successfully.</p>

        <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">

            <tr>
                <td style="padding: 10px; border: 1px solid #e5e7eb;"><b>Transaction Type</b></td>
                <td style="padding: 10px; border: 1px solid #e5e7eb;">Deposit</td>
            </tr>

            <tr>
                <td style="padding: 10px; border: 1px solid #e5e7eb;"><b>Deposited Amount</b></td>
                <td style="padding: 10px; border: 1px solid #e5e7eb; color: #16a34a; font-weight: bold;">
                    ₹{amount:,.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px; border: 1px solid #e5e7eb;"><b>Available Balance</b></td>
                <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold;">
                    ₹{new_balance:,.2f}
                </td>
            </tr>

        </table>

        <p style="margin-top: 20px;">
            Thank you for banking with <b>MyBank</b>.
        </p>

    </div>
    """

    # Send email using USER email
    background_tasks.add_task(
        send_email,
        user.email,
        "Deposit Successful",
        email_body
    )

    return {
        "success": True,
        "message": "Deposit completed successfully and email notification sent",
        "data": {
            "account_no": account.acc_no,
            "account_holder": account.acc_holder_name,
            "deposited_amount": amount,
            "previous_balance": previous_balance,
            "available_balance": new_balance,
            "email_sent_to": user.email
        }
    }

async def withdraw(id: int, amount: float, background_tasks: BackgroundTasks):
    """Withdraw money from account and send email notification"""

    # Find account
    account = await Accounts.find_one(Accounts.acc_no == id)

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with id {id} not found"
        )

    # Validate amount
    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Withdrawal amount must be positive"
        )

    # Check balance
    if amount > account.balance:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds for withdrawal"
        )

    # Get linked user
    user = await Users.find_one(Users.user_id == account.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Linked user not found"
        )

    # Store previous balance
    previous_balance = account.balance

    # Update balance
    account.balance -= amount
    new_balance = account.balance

    # Save account
    await account.save()

    # ---------------- EMAIL TEMPLATE ----------------
    email_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">

        <h2 style="color: #dc2626;">Withdrawal Alert</h2>

        <p>Dear <b>{account.acc_holder_name}</b>,</p>

        <p>A debit transaction has been processed from your account.</p>

        <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">

            <tr>
                <td style="padding: 10px; border: 1px solid #e5e7eb;"><b>Transaction Type</b></td>
                <td style="padding: 10px; border: 1px solid #e5e7eb;">Withdrawal</td>
            </tr>

            <tr>
                <td style="padding: 10px; border: 1px solid #e5e7eb;"><b>Withdrawn Amount</b></td>
                <td style="padding: 10px; border: 1px solid #e5e7eb; color: #dc2626; font-weight: bold;">
                    ₹{amount:,.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px; border: 1px solid #e5e7eb;"><b>Available Balance</b></td>
                <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold;">
                    ₹{new_balance:,.2f}
                </td>
            </tr>

        </table>

        <p style="margin-top: 20px;">
            If you did not authorize this transaction, please contact customer support immediately.
        </p>

    </div>
    """

    # Send email
    background_tasks.add_task(
        send_email,
        user.email,
        "Withdrawal Alert",
        email_body
    )

    return {
        "success": True,
        "message": "Withdrawal completed successfully and email notification sent",
        "data": {
            "account_no": account.acc_no,
            "account_holder": account.acc_holder_name,
            "withdrawn_amount": amount,
            "previous_balance": previous_balance,
            "available_balance": new_balance,
            "email_sent_to": user.email
        }
    }