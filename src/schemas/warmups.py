from uuid import UUID

from pydantic import BaseModel
from pydantic import validator


class WarmUpSummonSchema(BaseModel):
    """Схема призывалки"""

    id: UUID
    text: str


class WarmUpSummonCreateSchema(BaseModel):
    """Схема создания призывалки"""

    text: str

    @validator("text")
    def validate_text(cls, v: str) -> str:
        if "{}" not in v:
            raise ValueError("You don't specified place format")
        return v


class WarmupQueueSchema(BaseModel):
    """Схема очереди тренировок"""

    group_telegram_id: int
    user_ids: list[UUID]


class WarmupQueueCreateSchema(BaseModel):
    """Схема создания очереди тренировок"""

    user_ids: list[UUID]


class WarmupQueueUpdateSchema(BaseModel):
    """Схема обновления очереди тренировок"""

    user_ids: list[UUID]
