from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FeedbackCreateSchema(BaseModel):
    """Схема создания фидбека"""

    from_user_telegram_id: int
    message: str


class FeedbackSchema(BaseModel):
    """Схема фидбека"""

    id: UUID
    from_user_telegram_id: int
    message: str
