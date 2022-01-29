from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


class PrimaryKeyMixin:
    id = sa.Column(UUID, primary_key=True, index=True, default=uuid4, unique=True)


class TimeStampedMixin:
    created_at = sa.Column(sa.DateTime(timezone=True))
    updated_at = sa.Column(sa.DateTime(timezone=True))


class UserChangesMixin:
    created_by = sa.Column(UUID)
    updated_by = sa.Column(UUID)
