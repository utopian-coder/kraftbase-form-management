from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from app.models.form import Form
from app.schemas.form import FormCreate, FormInDB, FormSubmissionCreate, FormSubmissionInDB


class FormService:
    async def create_form(
        self,
        *,
        data: FormCreate,
        db: Session,
        # user: UserInDB
    ) -> FormInDB:
        new_form = Form(
            title=data.title,
            description=data.description,
            fields=[field.model_dump() for field in data.fields]
        )

        db.add(new_form)
        db.commit()
        db.refresh(new_form)

        return FormInDB(
            id=new_form.id,
            title=new_form.title,
            description=new_form.description,
            fields=new_form.fields
        )

    async def get_forms(
        self,
        *,
        db: Session,
        # user: Depends(authorize_user)
    ) -> list[FormInDB]:
        forms = db.query(Form).all()
        return TypeAdapter(list[FormInDB]).validate_python(forms)

    async def get_form(
        self,
        *,
        db: Session,
        form_id: UUID
    ) -> FormInDB:
        form = db.query(Form).filter(Form.id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")

        return FormInDB(
            id=form.id,
            title=form.title,
            description=form.description,
            fields=form.fields
        )

    async def delete_form(
        self,
        *,
        db: Session,
        form_id: UUID
    ) -> None:
        form = db.query(Form).filter(Form.id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        db.delete(form)

    async def submit_form(
        self,
        *,
        form_id: UUID,
        # user: UserInDB,
        db: Session,
        data: dict
    ) -> None:
        form = db.query(Form).filter(Form.id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")

        submission = FormSubmissionCreate(
            form_id=form_id,
            data=data,
            submitted_at=str(datetime.now(timezone.utc))
        )

        db.add(submission)
        db.commit()
        db.refresh(submission)

        return FormSubmissionInDB(
            id=submission.id,
            form_id=submission.form_id,
            data=submission.data,
            submitted_at=submission.submitted_at
        )

    async def get_submissions(
        self,
        *,
        form_id: UUID
    ) -> None:
        pass

form_service = FormService()
