import random
from typing import List, Literal, cast

import numpy as np
import numpy.typing as npt
from annoy import AnnoyIndex
from loguru import logger

from memes_service.config import MODEL_PATH, VECTOR_DIMENSIONS

ANNOY_METRIC = cast(Literal, "angular")


class ApproximateNearestNeighborsService:
    def __init__(self):
        self.annoy_model = AnnoyIndex(VECTOR_DIMENSIONS, ANNOY_METRIC)
        self.annoy_model.load(MODEL_PATH)

    def get_nearest_vectors_ids_by_vector(
        self,
        vector: npt.ArrayLike,
        number_of_vectors: int = 10,
    ) -> np.ndarray:
        vector_ids = self.annoy_model.get_nns_by_vector(vector, number_of_vectors)

        return np.array(
            [self.annoy_model.get_item_vector(vector_id) for vector_id in vector_ids],
        )

    def get_vectors_by_meme_ids(self, meme_ids: List[int]) -> np.ndarray:
        return np.array(
            [self.annoy_model.get_item_vector(meme_id) for meme_id in meme_ids],
        )

    @staticmethod
    def calculate_user_meme_vector(user_memes_features: np.ndarray) -> np.ndarray:
        return np.mean(user_memes_features, axis=0).astype("float32")

    def get_recommendations_from_small_model(
        self,
        user_reacted_memes_ids: List[int],
        user_vector: npt.ArrayLike,
    ) -> List[int]:
        numbers_of_all_memes = self.annoy_model.get_n_items()

        filtered_ids = random.sample(
            self.__get_filtered_ids(numbers_of_all_memes, user_reacted_memes_ids),
            numbers_of_all_memes // 4,
        )

        small_model = AnnoyIndex(VECTOR_DIMENSIONS, ANNOY_METRIC)
        for meme_id in filtered_ids:
            small_model.add_item(meme_id, self.annoy_model.get_item_vector(meme_id))

        small_model.build(10)
        logger.debug(user_vector)

        return small_model.get_nns_by_vector(user_vector, 50)

    def get_user_recommendations(
        self,
        user_liked_memes_ids: List[int],
        user_reacted_memes_ids: List[int],
    ) -> List[int]:
        user_memes_vectors = self.get_vectors_by_meme_ids(user_liked_memes_ids)
        user_memes_vector = self.calculate_user_meme_vector(user_memes_vectors)

        return self.get_recommendations_from_small_model(
            user_reacted_memes_ids,
            user_memes_vector,
        )

    @staticmethod
    def __get_filtered_ids(
        numbers_of_all_memes: int,
        memes_id_for_exclude: List[int],
    ) -> List[int]:
        return [
            meme_id
            for meme_id in range(numbers_of_all_memes)
            if meme_id not in memes_id_for_exclude
        ]
