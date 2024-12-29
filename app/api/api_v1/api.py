from fastapi import APIRouter

from .endpoints import auth, forms


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(forms.router, prefix="/forms", tags=["Form Management"])
