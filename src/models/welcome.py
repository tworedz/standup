from uuid import uuid4

import sqlalchemy as sa
from core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class WelcomeFile(Base):
    """"""

    __tablename__ = "welcomers"

    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)
    file_id = sa.Column(sa.String, unique=True)
    name = sa.Column(sa.String)
