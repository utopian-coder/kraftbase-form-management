import logging
from fastapi import FastAPI

import app

from app.settings.config import settings
from app.api.api_v1.api import api_router
from app.core.init_app import init_middlewares, register_exceptions

from app.core.log import configure_logging


configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=app.VERSION,
    debug=settings.DEBUG,
    root_path=settings.ROOT_PATH,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    contact=settings.CONTACT,
)

init_middlewares(app)
register_exceptions(app)


@app.get("/healthz", tags=["Liveliness"])
def health():
    return "OK"

app.include_router(api_router, prefix=settings.API_V1_STR)
