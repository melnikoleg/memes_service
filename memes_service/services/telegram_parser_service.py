import datetime
import re
from itertools import chain
from typing import Dict, List

import requests
from bs4 import BeautifulSoup, Tag
from loguru import logger

from memes_service.config import TELEGRAM_CHANNELS_LIST_URL
from memes_service.db.models.memes import MemesModel
from memes_service.services.approximate_nearest_neighbors_service import (
    ApproximateNearestNeighborsService,
)
from memes_service.services.clip_service_client import ClipServiceClient
from memes_service.services.meme_service import MemesService
from memes_service.services.storage_service import StorageService


class TelegramChannelParserService:
    def __init__(self):
        self.channel_urls = TELEGRAM_CHANNELS_LIST_URL
        self.clip_service_client = ClipServiceClient()
        self.__ann_service = ApproximateNearestNeighborsService()
        self.memes_service = MemesService()
        self.storage_service = StorageService()

    async def process_new_memes(self):
        memes_url_list = self.parse_telegram_channels()
        logger.debug(f"memes_url_list: {memes_url_list}")

        uploaded_memes = await self.storage_service.upload_memes_to_bucket(
            memes_url_list,
        )

        meme_bytes = self.__get_meme_bytes(uploaded_memes)

        meme_vectors = await self.get_memes_vectors(meme_bytes)
        logger.debug(f"Process: {meme_vectors}")

        memes_paths = [meme_vector.get("object_name") for meme_vector in meme_vectors]
        logger.debug(f"memes_paths: {memes_paths}")
        memes = await self.memes_service.add_memes_to_db(memes_paths)

        meme_vectors = self.__merge_memes_dicts_list(meme_vectors, memes)

        self.__ann_service.add_new_elements(meme_vectors)

    @staticmethod
    def __get_meme_bytes(memes_list: List[Dict]) -> List[Dict]:
        image_bytes = []

        for meme in memes_list:
            image_bytes.append(
                {
                    "meme_bytes": meme.get("meme_file"),
                    "object_name": meme.get("object_name"),
                },
            )

        return image_bytes

    async def get_memes_vectors(self, memes_bytes_list: List[Dict]) -> List[Dict]:
        meme_vectors = []
        for meme_byte in memes_bytes_list:
            meme_vector = await self.clip_service_client.get_image_vector(meme_byte)
            meme_vectors.append(meme_vector)
        return meme_vectors

    def parse_telegram_channels(self) -> List[str]:
        memes_url_list = []
        for channel_url in self.channel_urls:
            memes_url_list.extend(self.__parse_telegram_channel(channel_url))

        return memes_url_list

    @staticmethod
    def __parse_telegram_channel(channel_url: str) -> List[str]:
        memes_url_list = []
        page = requests.get(channel_url)
        soup = BeautifulSoup(page.text, "html.parser")
        all_memes = soup.findAll(
            class_="tgme_widget_message_wrap js-widget_message_wrap",
        )
        threshold_date = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        for tg_meme in all_memes:
            link = tg_meme.find("a", style=True)
            date_time_str = tg_meme.find("time")
            if link and date_time_str:
                date_time_obj = datetime.datetime.fromisoformat(
                    date_time_str.get("datetime"),
                )
                if date_time_obj.replace(tzinfo=None) > threshold_date:
                    link = link.get("style")
                    url = re.search("(?P<url>https?://[^\s']+)", link).group("url")
                    memes_url_list.append(url)

        return memes_url_list

    @staticmethod
    def __merge_memes_dicts_list(
        first_list: List[Dict],
        second_list: List[MemesModel],
        key: str = "object_name",
    ) -> List[Dict]:

        second_list = [{"meme_id": meme.id, key: meme.path} for meme in second_list]
        merged_dicts = {dictionary[key]: dictionary for dictionary in first_list}

        merged_list = []
        for dictionary in second_list:
            dict_key = dictionary[key]
            if dict_key in merged_dicts:
                merged_dicts[dict_key].update(dictionary)
                merged_list.append(merged_dicts[dict_key])

        return merged_list

    @staticmethod
    def __check_caption_for_ads(tags: Tag) -> bool:
        captions = tags.find_all(
            "div",
            {"class": "tgme_widget_message_text js-message_text"},
        )
        captions = [item.find("a") for item in captions]
        captions = list(filter(None, captions))
        return True if captions else None


def _range_with_end(start: int, stop: int, step: int = 1) -> List[int]:
    return list(chain(range(start, stop, step), (stop,)))
