from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Схема пользователя"""

    id: UUID
    telegram_id: int
    username: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    mention: Optional[str]


class UserCreateSchema(BaseModel):
    """Схема создания пользователя"""

    telegram_id: int
    username: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    mention: Optional[str]


class GroupSchema(BaseModel):
    """Схема группы"""

    id: UUID
    telegram_id: int
    name: Optional[str]


class GroupCreateSchema(BaseModel):
    """Схема создания группы"""

    telegram_id: int
    title: str


class UserGroupSchema(BaseModel):
    """схема пользователя в группе"""

    user_id: UUID
    group_id: UUID


class GroupMigrateSchema(BaseModel):
    """Схема миграции группы в супергруппу"""

    super_group_id: int
