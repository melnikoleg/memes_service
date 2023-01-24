import random
from typing import Dict, List, Literal, cast

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
        filtered_ids: List[int],
        user_vector: npt.ArrayLike,
    ) -> List[int]:
        small_model = AnnoyIndex(VECTOR_DIMENSIONS, ANNOY_METRIC)
        for meme_id in filtered_ids:
            small_model.add_item(meme_id, self.annoy_model.get_item_vector(meme_id))

        small_model.build(10)
        return small_model.get_nns_by_vector(user_vector, 5)

    def get_user_recommendations(
        self,
        user_liked_memes_ids: List[int],
        user_reacted_memes_ids: List[int],
    ) -> List[int]:
        user_memes_vectors = self.get_vectors_by_meme_ids(user_liked_memes_ids)
        user_memes_vector = self.calculate_user_meme_vector(user_memes_vectors)
        numbers_of_all_memes = self.annoy_model.get_n_items()

        filtered_ids = random.sample(
            self.__get_filtered_ids(numbers_of_all_memes, user_reacted_memes_ids),
            numbers_of_all_memes // 4,
        )
        recommendations_from_small_model = self.get_recommendations_from_small_model(
            filtered_ids,
            user_memes_vector,
        )
        random_memes = self.__get_random_memes(filtered_ids)
        recommendations = list(set(random_memes + recommendations_from_small_model))
        random.shuffle(recommendations)
        return recommendations

    def add_new_elements(self, meme_vectors: List[Dict]):
        new_model = self.__regenerate_model()
        for meme_vector in meme_vectors:

            new_model.add_item(
                meme_vector.get("meme_id"),
                meme_vector.get("image_vector"),
            )
        logger.debug("build new_model")

        new_model.build(10)
        new_model.save(MODEL_PATH)
        self.annoy_model = new_model

    def __regenerate_model(self) -> AnnoyIndex:
        model = AnnoyIndex(VECTOR_DIMENSIONS, ANNOY_METRIC)
        for id_item in range(self.annoy_model.get_n_items()):
            vector = self.annoy_model.get_item_vector(id_item)
            model.add_item(id_item, vector)

        return model

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

    @staticmethod
    def __get_random_memes(
        filtered_ids: list[int],
        number: int = 5,
    ) -> List[int]:
        return random.sample(filtered_ids, k=number)
