from typing import AsyncGenerator, List

from fastapi import Depends
from redis.asyncio import ConnectionPool, Redis
from starlette.requests import Request

from memes_service.settings import settings


async def get_redis_pool(
    request: Request,
) -> AsyncGenerator[Redis, None]:  # pragma: no cover
    """
    Returns connection pool.

    You can use it like this:

    >>> from redis.asyncio import ConnectionPool, Redis
    >>>
    >>> async def handler(redis_pool: ConnectionPool = Depends(get_redis_pool)):
    >>>     async with Redis(connection_pool=redis_pool) as redis:
    >>>         await redis.get('key')

    I use pools so you don't acquire connection till the end of the handler.

    :param request: current request.
    :returns:  redis connection pool.
    """
    return request.app.state.redis_pool


async def handler(redis_pool: ConnectionPool = Depends(get_redis_pool)):
    async with Redis(connection_pool=redis_pool) as redis:
        await redis.get("key")


def get_redis_pool():  # noqa: WPS440
    return ConnectionPool.from_url(
        str(settings.redis_url),
    )


async def get_len_user_queue(
    user_id: int,
    redis_pool=get_redis_pool(),
) -> int:
    async with Redis(connection_pool=redis_pool) as redis:
        return await redis.llen(str(user_id))


async def get_from_user_queue(
    user_id: int,
    redis_pool=get_redis_pool(),
):
    async with Redis(connection_pool=redis_pool) as redis:
        return await redis.lpop(str(user_id))


async def set_to_user_queue(
    user_id: int,
    memes_ids: List[int],
    redis_pool=get_redis_pool(),
):

    async with Redis(connection_pool=redis_pool) as redis:
        return await redis.lpush(str(user_id), *memes_ids)
