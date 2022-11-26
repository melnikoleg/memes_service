from typing import List

from memes_service.config import Reactions
from memes_service.services.approximate_nearest_neighbors_service import (
    ApproximateNearestNeighborsService,
)
from memes_service.services.meme_service import MemesService
from memes_service.services.reaction import ReactionService


class RecomendationSystem:
    def __init__(self):
        self.__ann_service = ApproximateNearestNeighborsService()
        self.__reaction_service = ReactionService()
        self.__memes_service = MemesService()

    async def get_memes_recommendation(self, user_id: int) -> List[int]:
        # get all reactions for exclude them
        user_reactions = await self.__reaction_service.get_user_reactions(user_id)
        user_reactions_ids = [user_reaction.meme_id for user_reaction in user_reactions]
        user_liked_memes_ids = [
            user_reaction.meme_id
            for user_reaction in user_reactions
            if user_reaction.reaction == Reactions.LIKE
        ]

        if user_reactions_ids:
            return self.__ann_service.get_user_recommendations(
                user_liked_memes_ids,
                user_reactions_ids,
            )

        return [meme.id for meme in await self.__memes_service.get_init_memes()]
