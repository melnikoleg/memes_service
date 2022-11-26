from fastapi.routing import APIRouter

from memes_service.web.api import echo, memes_controller, monitoring, reactions

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])

api_router.include_router(
    memes_controller.router,
    prefix="/meme_recommendation",
    tags=["meme_recommendation"],
)
api_router.include_router(reactions.router, prefix="/reactions", tags=["reactions"])
