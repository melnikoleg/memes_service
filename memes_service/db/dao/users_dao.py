from typing import List, Optional

from sqlalchemy import select

from memes_service.db.dependencies import get_session
from memes_service.db.models.users import UsersModel


class UsersDAO:
    def __init__(self):
        self.session = get_session()

    async def add_user_db(self, telegram_id: int) -> UsersModel:
        user = UsersModel(telegram_id=telegram_id)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_users_db(self) -> Optional[List[UsersModel]]:

        memes = await self.session.execute(
            select(UsersModel),
        )
        result = memes.scalars()
        await self.session.commit()
        if result:
            return result
        return None

    async def get_user_by_telegram_id_db(
        self,
        telegram_id: int,
    ) -> Optional[UsersModel]:

        query = select(UsersModel)
        query = query.where(UsersModel.telegram_id == telegram_id)
        rows = await self.session.execute(query)
        result = rows.scalars().first()
        await self.session.commit()
        if result:
            return result
        return None

    async def get_user_by_id_db(
        self,
        user_id: int,
    ) -> UsersModel:

        query = select(UsersModel)
        query = query.where(UsersModel.id == user_id)
        rows = await self.session.execute(query)
        return rows.scalars().first()
