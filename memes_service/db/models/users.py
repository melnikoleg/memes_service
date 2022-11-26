from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from memes_service.db.base import Base


class UsersModel(Base):

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = Column(Integer())

    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id
