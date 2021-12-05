from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Схема пользователя"""

    id: Optional[int]
    username: Optional[str]


class Group(BaseModel):
    """Схема группы"""

    id: int
    name: str


class UserGroup(BaseModel):
    """схема пользователя в группе"""
