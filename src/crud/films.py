import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from core.database import database
from crud.base import BaseCRUD
from models.films import FilmSetting
from schemas.films import FilmSettingUpdateOrCreateSchema
from schemas.films import FilmSettingSchema


class FilmCRUD(BaseCRUD):
    _model = FilmSetting
    _model_schema = FilmSettingSchema

    @classmethod
    async def get_channels(cls) -> list[FilmSettingSchema]:
        query = cls.get_base_query()
        return await cls.get_results(query)

    @classmethod
    async def get_channel_settings(cls, telegram_channel_id: int) -> FilmSettingSchema:
        query = cls.get_base_query().where(cls._model.telegram_channel_id == telegram_channel_id)
        result = await database.fetch_one(query)
        return cls.get_parsed_object(result)

    @classmethod
    async def update_or_create_channel_settings(cls, telegram_channel_id: int, data: FilmSettingUpdateOrCreateSchema) -> Optional[FilmSettingSchema]:
        values = {
            **cls.generate_id(),
            **cls.time_stamp(),
            **data.dict(),
            cls._model.telegram_channel_id.key: telegram_channel_id,
        }

        query = (
            insert(cls._model, values=values)
            .on_conflict_do_update(index_elements=["telegram_channel_id"], set_={
                cls._model.updated_at.key: datetime.datetime.now(),
                **data.dict(exclude_unset=True),
            })
            .returning(*cls._model.__table__.columns)
        )
        result = await database.fetch_one(query)

        return cls.get_parsed_object(result)
