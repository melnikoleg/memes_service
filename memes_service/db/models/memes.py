import datetime

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from memes_service.db.base import Base


class MemesModel(Base):

    __tablename__ = "memes"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    path = Column(String(length=200))
    created_date = Column(DateTime, default=datetime.datetime.now())
