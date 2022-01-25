import uuid
from typing import Generic

from core.database import Base


class BaseCRUD(Generic):
    _model = Base
    _model_schema = None

    @classmethod
    def generate_id(cls) -> dict:
        return {
            cls._model.id.key: uuid.uuid4(),
        }
