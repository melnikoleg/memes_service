from typing import Dict

import aiohttp

SERVICE_URL = "http://clip_service:8002/api"
POST_METHOD = "post"


class ClipServiceClient:
    @staticmethod
    async def __process_request(
        session: aiohttp.ClientSession(),
        method: str,
        endpoint: str,
        form,
    ) -> Dict:

        session_method = getattr(session, method)
        async with session_method(endpoint, data=form) as response:
            return await response.json()

    async def __service_request(self, method: str, endpoint: str, form) -> Dict:
        async with aiohttp.ClientSession() as session:
            return await self.__process_request(session, method, endpoint, form)

    async def get_image_vector(
        self,
        meme_bytes: Dict,
    ) -> Dict[float, str]:
        endpoint = f"{SERVICE_URL}/get_clip_image_vector_from_bytes/"
        form = aiohttp.FormData()
        object_name = meme_bytes.get("object_name")
        form.add_field("meme_bytes", meme_bytes.get("meme_bytes"), filename=object_name)
        form.add_field("object_name", object_name)

        return await self.__service_request(POST_METHOD, endpoint, form)
