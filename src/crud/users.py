import uuid
from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from aiogram import types
from asyncpg import UniqueViolationError
from core.database import database
from core.logging import logger
from crud.base import BaseCRUD
from models import Group
from models import User
from models import UserGroup
from pydantic import parse_obj_as
from schemas.users import GroupCreateSchema
from schemas.users import GroupSchema
from schemas.users import UserCreateSchema
from schemas.users import UserGroupSchema
from schemas.users import UserSchema


class UserCRUD(BaseCRUD):
    _model = User
    _model_schema = UserSchema

    @classmethod
    async def get_user(cls, user_telegram_id: str) -> Optional[UserSchema]:
        query = sa.select([cls._model]).where(cls._model.telegram_id == user_telegram_id)
        maybe = await database.fetch_one(query)
        return cls._get_parsed_object(maybe)

    @classmethod
    async def create_user(cls, user_data: UserCreateSchema) -> UserSchema:
        values = {
            **cls.generate_id(),
            **user_data.dict(),
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls._get_parsed_object(result)

    @classmethod
    async def update_user(cls, user_data: UserCreateSchema) -> UserSchema:
        values = {
            **user_data.dict(),
        }
        query = (
            sa.update(cls._model, values=values)
            .where(cls._model.telegram_id == user_data.telegram_id)
            .returning(*cls._model.__table__.columns)
        )
        result = await database.fetch_one(query)
        return cls._get_parsed_object(result)

    @classmethod
    async def get_users(cls) -> List[UserSchema]:
        query = sa.select([cls._model])
        result = await database.fetch_all(query)
        return parse_obj_as(List[UserSchema], result)

    @classmethod
    async def get_group_users(cls, chat_id: int) -> list[UserSchema]:
        query = (
            sa.select([cls._model])
            .select_from(sa.join(User, UserGroup).join(UserGroup, Group))
            .where(Group.telegram_id == chat_id)
        )
        return await cls.get_results(query)

    @classmethod
    async def get_random_user(cls) -> Optional[UserSchema]:
        query = cls.get_base_query().order_by(sa.func.random()).limit(1)
        result = await database.fetch_one(query)
        return UserSchema.parse_obj(result) if result else None


class GroupCRUD(BaseCRUD):
    _model = Group
    _model_schema = GroupSchema

    @classmethod
    async def get_groups(cls) -> list[GroupSchema]:
        query = cls.get_base_query()
        return await cls.get_results(query)

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
