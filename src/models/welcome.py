import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from core.database import Base


class WelcomeFile(Base):
    """"""

    __tablename__ = "users"

    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    file_id = sa.Column(sa.BigInteger, unique=True)
    username = sa.Column(sa.String)
    name = sa.Column(sa.String)
    surname = sa.Column(sa.String)
