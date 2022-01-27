from uuid import UUID

from pydantic import BaseModel


class WarmUpSummonSchema(BaseModel):
    """Схема призывалки"""

    id: UUID
    text: str


class WarmUpSummonCreateSchema(BaseModel):
    """Схема создания призывалки"""

    text: str
