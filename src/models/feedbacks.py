import sqlalchemy as sa
from core.database import Base
from models.base import PrimaryKeyMixin
from models.base import TimeStampedMixin
from models.base import UserChangesMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

__all__ = [
    "Feedback",
]


class Feedback(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Feedback"""

    __tablename__ = "feedbacks"

    from_user_telegram_id = sa.Column(sa.BigInteger)
    message = sa.Column(sa.String)
