from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


from app.settings.config import settings
from app.core.exceptions import APIException


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    app.add_middleware(GZipMiddleware)
    # @app.middleware("http")
    # async def set_secure_headers(request, call_next):
    #     response = await call_next(request)
    #     secure_headers().framework.fastapi(response)
    #     return response


def register_exceptions(app: FastAPI):
    app.add_exception_handler(APIException, APIException.handler)
