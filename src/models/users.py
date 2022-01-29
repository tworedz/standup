import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base
from models.base import PrimaryKeyMixin
from models.base import TimeStampedMixin
from models.base import UserChangesMixin


class User(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Пользователь"""

    __tablename__ = "users"

    telegram_id = sa.Column(sa.BigInteger, unique=True)
    username = sa.Column(sa.String)
    name = sa.Column(sa.String)
    surname = sa.Column(sa.String)
    mention = sa.Column(sa.String)


class Group(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Группа"""

    __tablename__ = "groups"
    telegram_id = sa.Column(sa.BigInteger, unique=True)
    title = sa.Column(sa.String)


class UserGroup(UserChangesMixin, TimeStampedMixin, PrimaryKeyMixin, Base):
    """Пользователь в группе"""

    __tablename__ = "user_groups"
    __table_args__ = (UniqueConstraint("user_id", "group_id"),)

    user_id = sa.Column(UUID, sa.ForeignKey("users.id", ondelete="CASCADE"))
    group_id = sa.Column(UUID, sa.ForeignKey("groups.id", ondelete="CASCADE"))
