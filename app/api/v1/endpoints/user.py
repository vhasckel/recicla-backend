from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ....models.user import UserCreate, UserUpdate, UserResponse
from ....services.user_service import user_service

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    return user_service.create_user(user_create=user_in)


@router.get("/", response_model=List[UserResponse])
def read_users():
    return user_service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: UUID):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user_in: UserUpdate):
    updated_user = user_service.update_user(user_id=user_id, user_update=user_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: UUID):
    deleted_user = user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
