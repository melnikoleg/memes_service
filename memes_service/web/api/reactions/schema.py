from pydantic import BaseModel


class MemeReactionsModelDTO(BaseModel):

    message: str


class MemeReactionsModelInputDTO(BaseModel):

    telegram_id: int
    meme_id: int
    reaction: str
