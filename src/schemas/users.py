from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Схема пользователя"""

    id: Optional[UUID]
    telegram_id: Optional[int]
    username: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class UserCreateSchema(BaseModel):
    """Схема создания пользователя"""

    telegram_id: Optional[int]
    username: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class Group(BaseModel):
    """Схема группы"""

    id: int
    name: str


class UserGroup(BaseModel):
    """схема пользователя в группе"""
