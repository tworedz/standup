from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from core.database import database
from models import WarmUp
from models import WarmupQueue
from models import WarmUpSummon
from schemas.warmups import WarmUpCreateSchema
from schemas.warmups import WarmUpSchema
from schemas.warmups import WarmUpUpdateSchema
from schemas.warmups import WarmupQueueCreateSchema
from schemas.warmups import WarmupQueueSchema
from schemas.warmups import WarmupQueueUpdateSchema
from schemas.warmups import WarmUpSummonCreateSchema
from schemas.warmups import WarmUpSummonSchema

from .base import BaseCRUD


class WarmUpSummonCRUD(BaseCRUD):
    _model = WarmUpSummon
    _model_schema = WarmUpSummonSchema

    @classmethod
    async def get_summoner_by_id(cls, summoner_id: UUID) -> Optional[WarmUpSummonSchema]:
        query = cls.get_base_query().where(cls._model.id == summoner_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def get_summoners(cls) -> List[WarmUpSummonSchema]:
        query = cls.get_base_query()
        return await cls.get_results(query)

    @classmethod
    async def get_random_summoner(cls) -> Optional[WarmUpSummonSchema]:
        query = cls.get_base_query().order_by(sa.func.random()).limit(1)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def create_summoner(cls, data: WarmUpSummonCreateSchema) -> WarmUpSummonSchema:
        summoner = data.text.replace("!", "\!")

        values = {
            **cls.generate_id(),
            cls._model.text.key: summoner,
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def delete_summoner(cls, summoner_id: UUID) -> None:
        query = sa.delete(cls._model).where(cls._model.id == summoner_id)
        await database.execute(query)


class WarmupQueueCRUD(BaseCRUD):
    _model = WarmupQueue
    _model_schema = WarmupQueueSchema

    @classmethod
    async def get_queue(cls, group_telegram_id: int) -> Optional[WarmupQueueSchema]:
        query = cls.get_base_query().where(cls._model.group_telegram_id == group_telegram_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def create_queue(
        cls, group_telegram_id: int, data: WarmupQueueCreateSchema
    ) -> WarmupQueueSchema:
        values = {
            **cls.generate_id(),
            **cls.time_stamp(),
            cls._model.group_telegram_id.key: group_telegram_id,
            cls._model.user_ids.key: data.user_ids,
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def update_queue(
        cls, group_telegram_id: int, data: WarmupQueueUpdateSchema
    ) -> Optional[WarmupQueueSchema]:
        values = {cls._model.user_ids.key: data.user_ids}

        query = (
            sa.update(cls._model, values=values)
            .where(
                cls._model.group_telegram_id == group_telegram_id,
            )
            .returning(*cls._model.__table__.columns)
        )
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)


class WarmUpCRUD(BaseCRUD):
    _model = WarmUp
    _model_schema = WarmUpSchema

    @classmethod
    async def get_warmup(cls, user_id: UUID, telegram_group_id: int) -> Optional[WarmUpSchema]:
        query = cls.get_base_query().where(
            sa.and_(
                cls._model.user_id == user_id, cls._model.telegram_group_id == telegram_group_id
            )
        ).order_by(cls._model.created_at.desc())
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def create_warmup(cls, data: WarmUpCreateSchema) -> WarmUpSchema:
        values = {
            **cls.generate_id(),
            **cls.time_stamp(),
            **data.dict(),
            cls._model.voted_user_ids.key: set(),
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def update_warmup(
        cls, user_id: UUID, telegram_group_id: int, data: WarmUpUpdateSchema
    ) -> WarmUpSchema:
        values = {
            cls._model.updated_at.key: datetime.now(),
            **data.dict(),
        }
        query = (
            sa.update(cls._model, values=values)
            .where(
                sa.and_(
                    cls._model.user_id == user_id, cls._model.telegram_group_id == telegram_group_id
                )
            )
            .returning(*cls._model.__table__.columns)
        )
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)
