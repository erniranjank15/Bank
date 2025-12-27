from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from repository import accounts as accounts_repo
from schemas import ShowAccount, UpdateAccountbyUser, UpdateAccountbyAdmin, CreateAccount
from auth import admin_only, get_current_user, user_or_admin, user_only 

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", status_code=200, response_model=List[ShowAccount])
async def all(current_user=Depends(admin_only)):
    return await accounts_repo.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowAccount)
async def create(request: CreateAccount, current_user=Depends(user_or_admin)):
    return await accounts_repo.create(request, current_user)    


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def destroy(id: int, current_user=Depends(admin_only)):
    return await accounts_repo.destroy(id)


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowAccount)
async def update(id: int, request: UpdateAccountbyUser, current_user=Depends(user_only)):
    return await accounts_repo.update(id, request)


@router.put("/{id}/admin", status_code=status.HTTP_202_ACCEPTED, response_model=ShowAccount)
async def admin_update(id: int, request: UpdateAccountbyAdmin, current_user=Depends(admin_only)):
    return await accounts_repo.admin_update(id, request)  


@router.get("/{id}", status_code=200, response_model=ShowAccount)
async def show(id: int, current_user=Depends(user_or_admin)):
    return await accounts_repo.show(id)


@router.post("/{id}/deposit", status_code=status.HTTP_200_OK, response_model=ShowAccount)
async def deposit(id: int, amount: float, current_user=Depends(user_or_admin)):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deposit amount must be greater than zero."
        )
    return await accounts_repo.deposit(id, amount)


@router.post("/{id}/withdraw", status_code=status.HTTP_200_OK, response_model=ShowAccount)
async def withdraw(id: int, amount: float, current_user=Depends(user_or_admin)):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Withdrawal amount must be greater than zero."
        )
    return await accounts_repo.withdraw(id, amount)