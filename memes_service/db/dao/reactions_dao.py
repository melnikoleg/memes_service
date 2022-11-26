import datetime
from typing import List, Optional

from sqlalchemy import select, update

from memes_service.db.dependencies import get_session
from memes_service.db.models.reactions import MemeReactionsModel


class ReactionsDAO:
    def __init__(self):
        self.session = get_session()

    async def add_user_reaction(
        self,
        meme_id: int,
        user_id: int,
        reaction: str,
    ) -> None:
        reaction = MemeReactionsModel(
            meme_id=meme_id,
            user_id=user_id,
            reaction=reaction,
            created_date=datetime.datetime.now(),
        )
        self.session.add(reaction)
        await self.session.commit()
        await self.session.refresh(reaction)

    async def get_user_reactions(
        self,
        user_id: int,
        reaction: str,
        limit: int = 100,
        offset: int = 100,
    ) -> List[MemeReactionsModel]:

        raw_dummies = await self.session.execute(
            select(MemeReactionsModel)
            .where(
                MemeReactionsModel.user_id == user_id,
                MemeReactionsModel.reaction == reaction,
            )
            .limit(limit)
            .offset(offset),
        )
        return raw_dummies.scalars().fetchall()

    async def get_all_user_reactions(self, user_id: int) -> List[MemeReactionsModel]:

        raw_dummies = await self.session.execute(
            select(MemeReactionsModel).where(
                MemeReactionsModel.user_id == user_id,
            ),
        )
        return raw_dummies.scalars().fetchall()

    async def get_user_reaction(
        self,
        user_id: int,
        meme_id: int,
    ) -> Optional[MemeReactionsModel]:
        raw_dummies = await self.session.execute(
            select(MemeReactionsModel).where(
                MemeReactionsModel.user_id == user_id,
                MemeReactionsModel.meme_id == meme_id,
            ),
        )
        return raw_dummies.scalars().first()

    async def update_user_reaction(
        self,
        user_reactions: MemeReactionsModel,
        reaction: str,
    ):
        await self.session.execute(
            update(MemeReactionsModel)
            .where(
                MemeReactionsModel.id == user_reactions.id,
            )
            .values({MemeReactionsModel.reaction: reaction}),
        )
        await self.session.commit()
