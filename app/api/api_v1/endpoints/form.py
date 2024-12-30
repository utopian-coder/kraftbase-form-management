from uuid import UUID
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, status, Body, Query, Depends

from app.models.form import Form
from app.core.database import db
from app import services, schemas
from app.schemas.auth import UserInDB
from app.services.user_session import UserSessionService
from app.core.exceptions import APIException
from app.schemas.form import FormCreate, FormCreateRequest, FormInDB, FormSubmissionCreate, FormSubmissionResponse, GetFormSubmissionsResponse
from app.services.form import form_service


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_form(
    data: Annotated[FormCreateRequest, Body(description="Form Data")],
    db: Annotated[Session, Depends(db.get_db)],
    user: Annotated[UUID, Depends(UserSessionService.authorize)]
) -> FormInDB:
    return await form_service.create_form(data=data, db=db, user=user)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_forms(
    db: Annotated[Session, Depends(db.get_db)],
    user= Depends(UserSessionService.authorize)
) -> list[FormInDB]:
    return await form_service.get_forms(db=db, user=user)

@router.get("/{form_id}", status_code=status.HTTP_200_OK)
async def get_form(
    db: Annotated[Session, Depends(db.get_db)],
    form_id: Annotated[UUID, Path(description="ID of the form")],
    _: Annotated[UUID, Depends(UserSessionService.authorize)]
) -> FormInDB:
    return await form_service.get_form(db=db, form_id=form_id)

@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
    db: Annotated[Session, Depends(db.get_db)],
    form_id: Annotated[UUID, Path(description="ID of the form")],
    _: Annotated[UUID, Depends(UserSessionService.authorize)]
) -> None:
    return await form_service.delete_form(db=db, form_id=form_id)

@router.post("/submit/{form_id}", status_code=status.HTTP_201_CREATED)
async def submit_form(
    form_id: Annotated[UUID, Path(description="ID of the form")],
    user: Annotated[UUID, Depends(UserSessionService.authorize)],
    data: Annotated[FormSubmissionCreate, Body(description="Form data")],
    db: Annotated[Session, Depends(db.get_db)]
) -> FormSubmissionResponse:
    return await form_service.submit_form(form_id=form_id, user=user, data=data, db=db)

@router.get("/submissions/{form_id}", status_code=status.HTTP_200_OK)
async def get_submissions(
    form_id: Annotated[UUID, Path(description="ID of the form")],
    db: Annotated[Session, Depends(db.get_db)],
    page: Annotated[int | None, Query(description="Page number")] = 1,
    limit: Annotated[int | None, Query(description="Number of items per page")] = 10
) -> GetFormSubmissionsResponse:
    return await form_service.get_submissions(form_id=form_id, page=page, limit=limit, db=db)  # type: ignore
