from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, status

from app.core.database import db
from app.services.auth import auth_service
from app.services.user_session import UserSessionService
from app.schemas.auth import LoginResponse, UserCreate, UserInDB, UserLogin


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: Annotated[UserCreate, Body(description="User data")],
    db: Annotated[Session, Depends(db.get_db)]
) -> UserInDB:
    return await auth_service.register(data=data, db=db)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: Annotated[UserLogin, Body(description="User login data")],
    db: Annotated[Session, Depends(db.get_db)]
) -> LoginResponse:
    return await auth_service.login(data=data, db=db)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    _ = Depends(UserSessionService.logout)
) -> dict:
    return {"message": "Logged out successfully."}
