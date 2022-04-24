import sqlalchemy as sa
from core.database import Base
from models.base import PrimaryKeyMixin
from models.base import TimeStampedMixin
from models.base import UserChangesMixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID

__all__ = [
    "WarmUp",
    "WarmUpSchedule",
    "WarmUpSummon",
    "WarmupQueue",
]


class WarmUp(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Тренировка"""

    __tablename__ = "warmups"

    user_id = sa.Column(UUID, sa.ForeignKey("users.id", ondelete="CASCADE"))
    telegram_group_id = sa.Column(sa.BigInteger)
    warmup_summon_id = sa.Column(UUID, sa.ForeignKey("warmup_summons.id", ondelete="CASCADE"))
    voted_user_ids = sa.Column(ARRAY(UUID))


class WarmUpSchedule(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Тренировки"""

    __tablename__ = "warmup_schedules"

    cron = sa.Column(sa.String)
    group_id = sa.Column(UUID)


class WarmUpSummon(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """призывалки"""

    __tablename__ = "warmup_summons"

    text = sa.Column(sa.String, unique=True)


class WarmupQueue(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Тренировка пользователя"""

    __tablename__ = "user_warmups"

    group_telegram_id = sa.Column(sa.BigInteger, unique=True)
    user_ids = sa.Column(ARRAY(UUID))
