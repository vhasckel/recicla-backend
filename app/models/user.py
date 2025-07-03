from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    passsword: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


"""ter um UserResponse garante que dados como a senha nao sejam expostas na API"""


class UserResponse(UserBase):
    id: UUID
    is_active: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    id: UUID
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
