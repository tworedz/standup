from uuid import UUID

from pydantic import BaseModel


class WarmUpSummonSchema(BaseModel):
    """Схема призывалки"""

    id: UUID
    summoner: str


class WarmUpSummonCreateSchema(BaseModel):
    """Схема создания призывалки"""

    summoner: str
