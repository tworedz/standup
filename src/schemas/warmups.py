from uuid import UUID

from pydantic import BaseModel
from pydantic import validator


class WarmUpSchema(BaseModel):
    """Схема тренировки"""

    id: UUID
    user_id: UUID
    telegram_group_id: int
    current_vote_count: int
    voted_user_ids: set[UUID]


class WarmUpCreateSchema(BaseModel):
    """Схема создания тренировки"""

    user_id: UUID
    telegram_group_id: int


class WarmUpUpdateSchema(BaseModel):
    """Схема изменения тренировки"""

    current_vote_count: int
    voted_user_ids: set[UUID]



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
