import sqlalchemy as sa
from core.database import Base
from models.base import PrimaryKeyMixin
from models.base import TimeStampedMixin
from models.base import UserChangesMixin
from sqlalchemy import UniqueConstraint

__all__ = [
    "FilmSetting",
]


class FilmSetting(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Настройки для фильма"""

    __tablename__ = "film_settings"
    __table_args__ = (
        UniqueConstraint("telegram_channel_id", "film_id"),
    )

    telegram_channel_id = sa.Column(sa.BigInteger, unique=True)
    film_id = sa.Column(sa.Integer)
    cron = sa.Column(sa.String)
    timeout = sa.Column(sa.Integer)
    is_enabled = sa.Column(sa.Boolean)
    forward_to = sa.Column(sa.String)
