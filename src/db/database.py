import importlib
import logging
from collections import defaultdict

from aiogram import types

from core.config import settings
from core.logging import logger


class Database:
    @classmethod
    async def get(cls, *args, **kwargs):
        pass

    @classmethod
    async def list(cls, table: str):  # noqa: A003
        pass

    @classmethod
    async def insert(cls, *args, **kwargs):
        pass

    @classmethod
    async def update(cls):
        pass

    @classmethod
    async def delete(cls):
        pass


class SqliteDatabase(Database):
    pass


class MemoryDatabase(Database):
    _database = defaultdict(list)

    @classmethod
    async def insert(cls, table: str, data: dict):
        cls._database[table].append(data)
        logger.debug("item inserted", table, data)

    @classmethod
    async def list(cls, table: str):
        return cls._database[table]


def get_database() -> Database:
    module, _, cls = settings.DATABASE_CLASS.rpartition(".")
    module = importlib.import_module(module)
    return getattr(module, cls)()


database = get_database()
