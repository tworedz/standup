from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from pydantic import parse_obj_as
from sqlalchemy.dialects.postgresql import insert

from core.database import database
from crud.base import BaseCRUD
from models import Group
from models import User
from models import UserGroup
from schemas.users import GroupCreateSchema
from schemas.users import GroupMigrateSchema
from schemas.users import GroupSchema
from schemas.users import UserCreateSchema
from schemas.users import UserSchema
from schemas.users import UserUpdateSchema


class UserCRUD(BaseCRUD):
    _model = User
    _model_schema = UserSchema

    @classmethod
    async def get_user_by_id(cls, user_id: UUID) -> Optional[UserSchema]:
        query = cls.get_base_query().where(cls._model.id == user_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def get_user_by_telegram_id(cls, telegram_id: str) -> Optional[UserSchema]:
        query = cls.get_base_query().where(cls._model.telegram_id == telegram_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def create_user(cls, user_data: UserCreateSchema) -> UserSchema:
        values = {
            **cls.generate_id(),
            **user_data.dict(),
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def update_user(cls, telegram_id: int, user_data: UserUpdateSchema) -> UserSchema:
        values = {
            **user_data.dict(),
        }
        query = (
            sa.update(cls._model, values=values)
            .where(cls._model.telegram_id == telegram_id)
            .returning(*cls._model.__table__.columns)
        )
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def get_users(cls) -> List[UserSchema]:
        query = sa.select([cls._model])
        result = await database.fetch_all(query)
        return parse_obj_as(List[UserSchema], result)

    @classmethod
    async def get_group_users(cls, telegram_id: int) -> list[UserSchema]:
        query = (
            sa.select([cls._model])
            .select_from(sa.join(User, UserGroup).join(Group))
            .where(Group.telegram_id == telegram_id)
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
    async def get_group_by_telegram_id(cls, telegram_id: int) -> Optional[GroupSchema]:
        query = sa.select([cls._model]).where(cls._model.telegram_id == telegram_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def update_or_create_group(cls, group_data: GroupCreateSchema) -> GroupSchema:
        values = {
            **cls.generate_id(),
            **cls.time_stamp(),
            **group_data.dict(),
        }

        query = (
            insert(cls._model, values=values)
            .returning(*cls._model.__table__.columns)
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={
                    cls._model.title.key: group_data.title,
                    cls._model.updated_at.key: datetime.now(),
                },
            )
        )
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def add_user_to_group(cls, user_id: UUID, group_id: UUID) -> None:
        values = {
            **cls.generate_id(),
            UserGroup.user_id.key: user_id,
            UserGroup.group_id.key: group_id,
        }

        query = insert(UserGroup, values=values).on_conflict_do_nothing()
        await database.fetch_one(query)

    @classmethod
    async def migrate_to_super_group(
        cls, telegram_id: str, data: GroupMigrateSchema
    ) -> Optional[GroupSchema]:
        values = {
            cls._model.telegram_id.key: data.super_group_id,
        }
        query = sa.update(cls._model, values=values).where(cls._model.telegram_id == telegram_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)
