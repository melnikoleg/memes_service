from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from memes_service.services.user_service import UsersService

app = FastAPI()


# class UserMiddleware:
#     async def __call__(self, request: Request, call_next):
#         users_service = UsersService()
#         # json = await request.json()
#         # telegram_id = json.get("telegram_id")
#         # logger.debug(telegram_id)
#         request.meme_user = await users_service.get_or_create_user_by_telegram_id(123)
#
#         return await call_next(request)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     users_service = UsersService()
#     json = await request.json()
#     telegram_id = json.get("telegram_id")
#     logger.debug(telegram_id)
#     user = await users_service.get_or_create_user_by_telegram_id(telegram_id)
#     request.state.meme_user = user.id
#
#     response = await call_next(request)
#     return response


class UserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.users_service = UsersService()

    async def set_body(self, request: Request):
        receive_ = await request._receive()  # noqa: WPS120

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)
        json = await request.json()
        telegram_id = json.get("telegram_id")
        user = await self.users_service.get_or_create_user_by_telegram_id(telegram_id)
        request.state.meme_user = user
        return await call_next(request)
