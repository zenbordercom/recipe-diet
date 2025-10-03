from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.base_class import Base
from app.db.session import engine


def create_application() -> FastAPI:
    app = FastAPI(title=settings.project_name, debug=settings.debug)

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    app.include_router(api_router)
    return app


app = create_application()
