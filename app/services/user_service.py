from typing import List, Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime, timezone

from ..models.user import UserCreate, UserUpdate, UserInDB, UserResponse
from ..core.security import get_password_hash
from fastapi import HTTPException, status


class UserService:
    def __init__(self):
        """dicionario em memoria para simular banco de dados"""
        self.db: Dict[UUID, UserInDB] = {}

    def get_user_by_id(self, user_id: UUID) -> Optional[UserInDB]:
        return self.db.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        for user in self.db.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self) -> List[UserInDB]:
        return list(self.db.values())

    def create_user(self, user_create: UserCreate) -> UserInDB:
        if self.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = get_password_hash(user_create.password)
        now = datetime.now(timezone.utc)

        new_user = UserInDB(
            id=uuid4(),
            **user_create.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
            created_at=now,
            updated_at=now
        )
        self.db[new_user.id] = new_user
        return new_user

    def update_user(self, user_id: UUID, user_update: UserUpdate) -> Optional[UserInDB]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            user.hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]

        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)
        self.db[user.id] = user
        return user

    def delete_user(self, user_id: UUID) -> Optional[UserInDB]:
        if user_id in self.db:
            return self.db.pop(user_id)
        return None


user_service = UserService()
