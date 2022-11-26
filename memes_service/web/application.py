from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from memes_service.logger import configure_logging
from memes_service.web.api.router import api_router
from memes_service.web.lifetime import register_shutdown_event, register_startup_event
from memes_service.web.middleware import UserMiddleware


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="memes_service",
        description="",
        version=metadata.version("memes_service"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # my_middleware = UserMiddleware()
    # app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)
    app.add_middleware(UserMiddleware)
    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
