from typing import List

from memes_service.config import Reactions
from memes_service.db.dao.reactions_dao import ReactionsDAO
from memes_service.db.models.reactions import MemeReactionsModel


class ReactionService:
    def __init__(self):
        self.reactions_dao = ReactionsDAO()

    async def get_user_reactions(self, user_id: int) -> List[MemeReactionsModel]:
        return await self.reactions_dao.get_all_user_reactions(user_id)

    async def get_last_liked_memes(self, user_id: int) -> List[int]:
        memes_reactions = await self.reactions_dao.get_user_reactions(
            user_id,
            Reactions.LIKE,
        )
        return [memes_reaction.meme_id for memes_reaction in memes_reactions]

    async def set_or_update_user_reaction(
        self,
        meme_id: int,
        user_id: int,
        reaction: str,
    ):
        user_reactions = await self.reactions_dao.get_user_reaction(user_id, meme_id)
        if user_reactions:
            await self.reactions_dao.update_user_reaction(user_reactions, reaction)
            return

        await self.reactions_dao.add_user_reaction(meme_id, user_id, reaction)
