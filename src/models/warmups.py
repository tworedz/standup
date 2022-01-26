from sqlalchemy.dialects.postgresql import UUID

from core.database import Base
import sqlalchemy as sa
from uuid import uuid4


class WarmUpSchedule(Base):
    """Тренировки"""

    __tablename__ = "warmup_schedules"

    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    cron = sa.Column(sa.String)
    group_id = sa.Column(UUID)


class WarmUpSummon(Base):
    """призывалки"""

    __tablename__ = "warmup_summons"

    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    summoner = sa.Column(sa.String)
