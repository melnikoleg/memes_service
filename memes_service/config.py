class Reactions:
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    NOTHING = "NOTHING"


VECTOR_DIMENSIONS = 512
MODEL_PATH = "/app/src/models/meme_model.ann"

DEFAULT_LIMIT_QUEUE_MEMES = 20


TELEGRAM_CHANNELS_LIST = [
    "PeeAcE_DaTa",
    "memasy",
    "mememanufactory",
    "fastfoodmemes",
    "ebanistika",
    "oh_ffs",
]
TELEGRAM_CHANNELS_LIST_URL = [
    f"https://t.me/s/{channel_name}" for channel_name in TELEGRAM_CHANNELS_LIST
]
