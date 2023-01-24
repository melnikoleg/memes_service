from loguru import logger

from memes_service.config import DEFAULT_LIMIT_QUEUE_MEMES
from memes_service.services.recomendation_module import RecomendationSystem
from memes_service.services.redis.dependency import (
    get_len_user_queue,
    set_to_user_queue,
)
from memes_service.services.user_service import UsersService


class QueueService:
    def __init__(self):

        self.recommendation_system = RecomendationSystem()
        self.users_service = UsersService()

    async def process_queues_all_users(self):

        users_ids = await self.users_service.get_users_ids()

        for user_id in users_ids:
            user_queue_len = await get_len_user_queue(user_id)

            if user_queue_len < DEFAULT_LIMIT_QUEUE_MEMES:
                logger.debug(f"Process: {user_id}")

                memes_recommendation = (
                    await self.recommendation_system.get_memes_recommendation(user_id)
                )
                await set_to_user_queue(user_id, memes_recommendation)
