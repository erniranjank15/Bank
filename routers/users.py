from fastapi import APIRouter, Depends, status
from typing import List
from repository import users as users_repo
from schemas import ShowUser, CreateUser as User
from auth import admin_only, get_current_user, user_or_admin, user_only

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create(request: User):
    return await users_repo.create_user_with_account(request)  


@router.get("/", status_code=200, response_model=List[ShowUser])
async def all(current_user=Depends(admin_only)):
    return await users_repo.get_all_users()  


@router.get("/{user_id}", status_code=200, response_model=ShowUser)
async def get_user(user_id: int, current_user=Depends(user_or_admin)):
    return await users_repo.get_user_by_id(user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user=Depends(admin_only)):
    return await users_repo.delete_user(user_id)


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowUser)
async def update_user(user_id: int, request: User, current_user=Depends(user_or_admin)):
    return await users_repo.update_user(user_id, request)