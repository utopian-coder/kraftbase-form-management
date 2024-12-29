from uuid import UUID
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, status, Body, Query, Depends

from app.models.form import Form
from app.core.database import db
from app import services, schemas
from app.schemas.auth import UserInDB
from app.services.user_session import UserSessionService
from app.utils.session import session
from app.core.exceptions import APIException
from app.schemas.form import FormCreate, FormInDB


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_form(
    data: Annotated[FormCreate, Body(description="Form Data")],
    db: Annotated[Session, Depends(db.get_db)],
    user: Annotated[UserInDB, Depends(UserSessionService.authorize)]
) -> FormInDB:
    new_form = Form(
        title=data.title,
        description=data.description,
        fields=[field.model_dump() for field in data.fields]
    )

    db.add(new_form)
    db.commit()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_forms(
    db: Annotated[Session, Depends(db.get_db)],
    user: Depends(authorize)
) -> list[FormInDB]:
    pass

@router.get("/{form_id}", status_code=status.HTTP_200_OK)
async def get_form(
    db: Annotated[Session, Depends(db.get_db)],
    form_id: Annotated[UUID, Path(description="ID of the form")]
) -> FormInDB:
    pass

@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
    db: Annotated[Session, Depends(db.get_db)],
    form_id: Annotated[UUID, Path(description="ID of the form")]
) -> None:
    pass

@router.post("/submit/{form_id}", status_code=status.HTTP_201_CREATED)
async def submit_form(
    form_id: Annotated[UUID, Path(description="ID of the form")],
    # user: Depends(authorize_user),
    data: Annotated[dict, Body(description="Form data")]
) -> None:
    pass

@router.get("/submissions/{form_id}", status_code=status.HTTP_200_OK)
async def get_submissions(
    form_id: Annotated[UUID, Path(description="ID of the form")],
    page: Annotated[int | None, Query(description="Page number")] = 1,
    limit: Annotated[int | None, Query(description="Number of items per page")] = 10
):  # page and limit needed
    pass
