import uuid
from typing import Any
from typing import List
from typing import Optional
from typing import TypeVar

import sqlalchemy as sa
from core.database import Base
from core.database import database
from pydantic import BaseModel
from pydantic import parse_obj_as
from sqlalchemy.sql import Select

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class BaseCRUD:
    _model = Base
    _model_schema = BaseModelType

    @classmethod
    def get_base_query(cls) -> Select:
        return sa.select([cls._model])

    @classmethod
    def generate_id(cls) -> dict:
        return {
            cls._model.id.key: uuid.uuid4(),
        }

    @classmethod
    def _get_parsed_object(cls, obj: Optional[Any]) -> Optional[BaseModelType]:
        if obj is None:
            return None
        return cls._model_schema.parse_obj(obj)

    @classmethod
    async def get_results(cls, query: Select) -> List[BaseModelType]:
        result = await database.fetch_all(query)
        return parse_obj_as(List[cls._model_schema], result)
