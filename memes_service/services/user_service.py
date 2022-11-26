from typing import List

from memes_service.db.dao.users_dao import UsersDAO
from memes_service.db.models.users import UsersModel
from memes_service.services.meme_service import MemesService
from memes_service.services.redis.dependency import set_to_user_queue


class UsersService:
    def __init__(
        self,
    ):
        self.__memes_service = MemesService()
        self.__users_dao = UsersDAO()

    async def get_users_ids(self) -> List[int]:
        users = await self.__users_dao.get_users_db()

        return [user.id for user in users]

    async def get_user_by_id(self, user_id: int) -> UsersModel:
        return await self.__users_dao.get_user_by_id_db(user_id)

    async def create_user(self, telegram_id) -> UsersModel:
        user = await self.__users_dao.add_user_db(telegram_id)
        init_memes = [meme.id for meme in await self.__memes_service.get_init_memes()]
        await set_to_user_queue(user.id, init_memes)
        return user

    async def get_or_create_user_by_telegram_id(
        self,
        telegram_id: int,
    ) -> UsersModel:
        user = await self.__users_dao.get_user_by_telegram_id_db(telegram_id)

        if user:
            return user

        return await self.create_user(telegram_id)
