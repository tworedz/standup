import uuid
from typing import List
from uuid import UUID

import sqlalchemy as sa
from asyncpg import UniqueViolationError
from pydantic import parse_obj_as

from core.database import database
from aiogram import types

from core.logging import logger
from crud.base import BaseCRUD
from models import Group, UserGroup
from models import User
from schemas.users import UserSchema, UserCreateSchema, GroupCreateSchema, GroupSchema, UserGroupSchema


class UserCRUD(BaseCRUD):
    _model = User
    _model_schema = UserSchema

    @classmethod
    async def get_or_create_user(cls, user_data: UserCreateSchema) -> UserSchema:
        query = sa.select([cls._model]).where(cls._model.telegram_id == user_data.telegram_id)
        maybe = await database.fetch_one(query)
        if maybe:
            return cls._get_parsed_object(maybe)

        values = {
            **cls.generate_id(),
            **user_data.dict(),
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls._get_parsed_object(result)

    @classmethod
    async def get_users(cls) -> List[UserSchema]:
        query = sa.select([cls._model])
        result = await database.fetch_all(query)
        return parse_obj_as(List[UserSchema], result)


class GroupCRUD(BaseCRUD):
    _model = Group
    _model_schema = GroupSchema

    @classmethod
    async def get_or_create_group(cls, group_data: GroupCreateSchema) -> GroupSchema:
        query = sa.select([cls._model]).where(cls._model.telegram_id == group_data.telegram_id)
        maybe = await database.fetch_one(query)
        if maybe:
            return cls._get_parsed_object(maybe)

        values = {
            **cls.generate_id(),
            **group_data.dict(),
        }

        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls._get_parsed_object(result)

    @classmethod
    async def add_user_to_group(cls, user_id: UUID, group_id: UUID) -> None:
        values = {
            **cls.generate_id(),
            UserGroup.user_id.key: user_id,
            UserGroup.group_id.key: group_id,
        }

        query = sa.insert(UserGroup, values=values)
        try:
            await database.fetch_one(query)
        except UniqueViolationError as e:
            logger.info("This user already in this group", error=e)
