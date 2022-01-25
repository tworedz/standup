import uuid
from typing import List

import sqlalchemy as sa
from pydantic import parse_obj_as

from core.database import database
from aiogram import types

from crud.base import BaseCRUD
from models import Group
from models import User
from schemas.users import UserSchema, UserCreateSchema


class UserCRUD(BaseCRUD):
    _model = User

    @classmethod
    async def get_or_create_user(cls, user_data: UserCreateSchema) -> UserSchema:
        query = sa.select([cls._model]).where(cls._model.telegram_id == user_data.telegram_id)
        maybe_user = await database.fetch_one(query)
        if maybe_user:
            return UserSchema.parse_obj(maybe_user)

        values = {
            **cls.generate_id(),
            **user_data.dict(),
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return UserSchema.parse_obj(result)

    @classmethod
    async def get_users(cls) -> List[UserSchema]:
        query = sa.select([cls._model])
        result = await database.fetch_all(query)
        return parse_obj_as(List[UserSchema], result)


class GroupCRUD(BaseCRUD):
    _model = Group

    @classmethod
    async def get_or_create_group(cls, group_data: ...) -> ...:
        pass
