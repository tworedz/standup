from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from core.database import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    """Пользователь"""

    __tablename__ = "users"

    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    telegram_id = sa.Column(sa.BigInteger, unique=True)
    username = sa.Column(sa.String)
    name = sa.Column(sa.String)
    surname = sa.Column(sa.String)
    mention = sa.Column(sa.String)


class Group(Base):
    """Группа"""

    __tablename__ = "groups"
    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    telegram_id = sa.Column(sa.BigInteger, unique=True)
    title = sa.Column(sa.String)


class UserGroup(Base):
    """Пользователь в группе"""

    __tablename__ = "user_groups"
    __table_args__ = (UniqueConstraint("user_id", "group_id"),)

    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    user_id = sa.Column(UUID)
    group_id = sa.Column(UUID)
