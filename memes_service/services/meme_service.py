from typing import List

from memes_service.config import DEFAULT_LIMIT_QUEUE_MEMES
from memes_service.db.dao.memes_dao import MemesDAO
from memes_service.db.dao.reactions_dao import ReactionsDAO
from memes_service.db.models.memes import MemesModel
from memes_service.db.models.reactions import MemeReactionsModel


class MemesService:
    def __init__(self):
        self.__memes_dao = MemesDAO()
        self.__reactions_dao = ReactionsDAO()

    def add_meme_to_db(self, path: str):
        self.__memes_dao.add_meme(path)

    async def get_meme_from_db(self, meme_id: int) -> MemesModel:
        return await self.__memes_dao.get_meme(meme_id)

    async def get_memes_by_user_reaction(
        self,
        user_id: int,
        reaction: str,
    ) -> List[MemeReactionsModel]:
        return await self.__reactions_dao.get_user_reactions(
            user_id,
            reaction,
        )

    async def get_memes_by_user_reacted(
        self,
        user_id: int,
    ) -> List[MemesModel]:
        memes_reacted = await self.__reactions_dao.get_all_user_reactions(user_id)
        memes_id = [memes_reaction.meme_id for memes_reaction in memes_reacted]

        return await self.__memes_dao.get_memes_by_ids(memes_id)

    async def get_init_memes(
        self,
        limit: int = DEFAULT_LIMIT_QUEUE_MEMES,
    ) -> List[MemesModel]:
        return await self.__memes_dao.get_random_memes(limit)
