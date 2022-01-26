from typing import List

import sqlalchemy as sa

from .base import BaseCRUD
from core.database import database
from models import WarmUpSummon
from schemas.warmups import WarmUpSummonSchema, WarmUpSummonCreateSchema


class WarmUpSummonCRUD(BaseCRUD):
    _model = WarmUpSummon
    _model_schema = WarmUpSummonSchema

    @classmethod
    async def get_summoners(cls) -> List[WarmUpSummonSchema]:
        query = cls.get_base_query()
        return await cls.get_results(query)

    @classmethod
    async def create_summoner(cls, data: WarmUpSummonCreateSchema) -> WarmUpSummonSchema:
        summoner = data.summoner.replace("$me", "{}")

        values = {
            **cls.generate_id(),
            cls._model.summoner.key: summoner,
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls._get_parsed_object(result)
