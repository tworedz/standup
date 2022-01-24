import databases
from core.config import settings
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

database = databases.Database(str(settings.DB_URI))

meta = MetaData()

Base = declarative_base(metadata=meta)
metadata = Base.metadata
