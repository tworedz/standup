from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from pydantic import parse_obj_as
from sqlalchemy.dialects.postgresql import insert

from core.database import database
from crud.base import BaseCRUD
from models import Group
from models import User
from models import UserGroup
from models.feedbacks import Feedback
from schemas.feedbacks import FeedbackCreateSchema
from schemas.feedbacks import FeedbackSchema
from schemas.users import GroupCreateSchema
from schemas.users import GroupMigrateSchema
from schemas.users import GroupSchema
from schemas.users import UserCreateSchema
from schemas.users import UserSchema
from schemas.users import UserUpdateSchema


class FeedbackCRUD(BaseCRUD):
    _model = Feedback
    _model_schema = FeedbackSchema

    @classmethod
    async def get_feedbacks(cls) -> List[FeedbackSchema]:
        query = cls.get_base_query()
        return await cls.get_results(query)

    @classmethod
    async def create_feedback(cls, data: FeedbackCreateSchema) -> Optional[FeedbackSchema]:
        values = {
            **cls.generate_id(),
            **cls.time_stamp(),
            **data.dict(),
        }

        query = sa.insert(cls._model, values=values).returning(*cls._model.__table__.columns)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)
