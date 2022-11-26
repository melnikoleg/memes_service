from pydantic import BaseModel


class MemesModelDTO(BaseModel):

    meme_path: str
    meme_id: int

    class Config:
        orm_mode = True


class MemesModelInputDTO(BaseModel):

    telegram_id: int
