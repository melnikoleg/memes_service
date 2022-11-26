from fastapi import APIRouter, Request

from memes_service.services.meme_service import MemesService
from memes_service.services.redis.dependency import get_from_user_queue
from memes_service.web.api.memes_controller.schema import (
    MemesModelDTO,
    MemesModelInputDTO,
)

router = APIRouter()


@router.post("/", response_model=MemesModelDTO)
async def meme_recommendation(request: Request, incoming_message: MemesModelInputDTO):
    meme_service = MemesService()
    user = request.state.meme_user

    meme_id = await get_from_user_queue(user.id)

    meme = await meme_service.get_meme_from_db(int(meme_id))
    return {"meme_id": meme.id, "meme_path": meme.path}
