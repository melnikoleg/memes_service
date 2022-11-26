from fastapi import APIRouter, Request

from memes_service.services.reaction import ReactionService
from memes_service.web.api.reactions.schema import (
    MemeReactionsModelDTO,
    MemeReactionsModelInputDTO,
)

router = APIRouter()


@router.post("/", response_model=MemeReactionsModelDTO)
async def meme_reaction(request: Request, incoming_message: MemeReactionsModelInputDTO):
    reaction_service = ReactionService()
    user = request.state.meme_user
    meme_id = incoming_message.meme_id
    reaction = incoming_message.reaction
    await reaction_service.set_or_update_user_reaction(meme_id, user.id, reaction)
    return {"message": "ok"}
