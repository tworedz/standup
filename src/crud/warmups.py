from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from core.database import database
from models import WarmUpSummon
from schemas.warmups import WarmUpSummonCreateSchema
from schemas.warmups import WarmUpSummonSchema

from .base import BaseCRUD


class WarmUpSummonCRUD(BaseCRUD):
    _model = WarmUpSummon
    _model_schema = WarmUpSummonSchema

    @classmethod
    async def get_summoners(cls) -> List[WarmUpSummonSchema]:
        query = cls.get_base_query()
        return await cls.get_results(query)

    @classmethod
    async def get_random_summoner(cls) -> Optional[WarmUpSummonSchema]:
        query = cls.get_base_query().order_by(sa.func.random()).limit(1)
        result = await database.fetch_one(query)
        return WarmUpSummonSchema.parse_obj(result) if result else None

    @classmethod
    async def create_summoner(cls, data: WarmUpSummonCreateSchema) -> WarmUpSummonSchema:
        summoner = data.text.replace("$me", "{}")
        summoner = summoner.replace("!", "\!")

        values = {
            **cls.generate_id(),
            cls._model.text.key: summoner,
        }
        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls._get_parsed_object(result)

    @classmethod
    async def delete_summoner(cls, summoner_id: UUID) -> None:
        query = sa.delete(cls._model).where(cls._model.id == summoner_id)
        await database.execute(query)
