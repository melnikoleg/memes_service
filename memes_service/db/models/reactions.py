import datetime

from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from memes_service.db.base import Base


class MemeReactionsModel(Base):

    __tablename__ = "meme_reactions"
    __table_args__ = (
        UniqueConstraint("user_id", "meme_id", name="uq_user_id_meme_id"),
    )

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer(), ForeignKey("users.id"))
    meme_id = Column(Integer(), ForeignKey("memes.id"))
    reaction = Column(String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
