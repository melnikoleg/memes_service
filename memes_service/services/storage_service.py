import uuid
from typing import Dict, List

import boto3
import requests

from memes_service.settings import settings

BUCKET_NAME = "memes"


class StorageService:
    def __init__(
        self,
    ):
        self.bucket_name = BUCKET_NAME
        session = boto3.session.Session()
        self.storage_client = session.client(
            service_name="s3",
            aws_access_key_id=settings.ACCESS_KEY_ID,
            aws_secret_access_key=settings.SECRET_ACCESS_KEY,
            endpoint_url=settings.ENDPOINT,
            region_name="eu-central-1",
        )

    async def upload_memes_to_bucket(self, memes_links: List[str]) -> List[Dict]:
        response = []
        for memes_link in memes_links:
            response.append(await self.upload_meme_to_bucket(memes_link))
        return response

    async def upload_meme_to_bucket(self, meme_url: str) -> Dict:
        meme_request = requests.get(meme_url, stream=True)
        meme_request_raw = meme_request.raw
        meme_file = meme_request_raw.read()

        object_name = f"{str(uuid.uuid1())}.{self.__get_file_extension(meme_url)}"

        self.storage_client.upload_fileobj(
            meme_request_raw,
            self.bucket_name,
            object_name,
        )

        return {
            "object_name": object_name,
            "meme_file": meme_file,
        }

    async def get_meme_from_bucket(self, meme: str) -> bytes:
        s3_response_object = self.storage_client.get_object(
            Bucket=self.bucket_name,
            Key=meme,
        )
        return s3_response_object["Body"].read()

    @staticmethod
    def __get_file_extension(url: str) -> str:
        return url.split(".")[-1]
