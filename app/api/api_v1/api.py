from fastapi import APIRouter

from .endpoints import auth, form


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(form.router, prefix="/form", tags=["Form Management"])
