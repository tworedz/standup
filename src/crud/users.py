from typing import List

from db.database import Database, database
from aiogram import types

from schemas.users import UserSchema


class UserCRUD:
    _table = "users"
    @classmethod
    async def create_user(cls, user: UserSchema) -> None:
        await database.insert(cls._table, user)

    @classmethod
    async def get_users(cls) -> List[UserSchema]:
        return await database.list(cls._table)
