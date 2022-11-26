from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from memes_service.settings import settings


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Create and get database session.")
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


engine = create_async_engine(
    str(settings.db_url),
    echo=settings.db_echo,
    pool_pre_ping=True,
)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency
def get_session():
    return async_session()
