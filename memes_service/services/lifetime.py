from fastapi import FastAPI

from memes_service.services.storage_service import StorageService


def init_storage_service(app: FastAPI) -> None:  # pragma: no cover
    app.state.storage_service = StorageService()
