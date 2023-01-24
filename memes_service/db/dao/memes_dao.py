import datetime
from typing import List, Optional

from sqlalchemy import func, select

from memes_service.db.dependencies import get_session
from memes_service.db.models.memes import MemesModel


class MemesDAO:
    def __init__(self):
        self.session = get_session()

    async def add_meme(self, path: str) -> MemesModel:
        meme = MemesModel(path=path, created_date=datetime.datetime.now())
        self.session.add(meme)
        await self.session.commit()
        await self.session.refresh(meme)
        return meme

    async def get_memes(self, limit: int, offset: int) -> List[MemesModel]:
        memes = await self.session.execute(
            select(MemesModel).limit(limit).offset(offset),
        )
        return memes.scalars().fetchall()

    async def get_memes_by_ids(
        self,
        memes_ids: List[int],
        limit: int = 10,
        offset: int = 10,
    ) -> List[MemesModel]:

        memes = await self.session.execute(
            select(MemesModel)
            .where(MemesModel.id in memes_ids)
            .limit(limit)
            .offset(offset),
        )

        return memes.scalars().fetchall()

    async def get_meme(
        self,
        meme_id: int,
    ) -> Optional[MemesModel]:
        query = select(MemesModel)
        query = query.where(MemesModel.id == meme_id)
        rows = await self.session.execute(query)
        result = rows.scalars().first()

        await self.session.commit()
        if result:
            return result
        return None

    async def get_random_memes(self, limit: int) -> List[MemesModel]:

        memes = await self.session.execute(
            select(MemesModel).order_by(func.random()).limit(limit),
        )
        return memes.scalars().fetchall()
