from typing import Any

from pydantic import BaseModel


class MemesModelDTO(BaseModel):

    meme_path: str
    meme_id: int
    meme_image: Any

    class Config:
        orm_mode = True


class MemesModelInputDTO(BaseModel):

    telegram_id: int
