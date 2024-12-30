from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from app.models.form import Form, FormSubmission
from app.schemas.form import FormCreateRequest, FormFieldResponse, FormInDB, FormSubmissionCreate, FormSubmissionDataForGetFormSubmissionResponse, FormSubmissionInDB, FormSubmissionResponse, GetFormSubmissionsResponse


class FormService:
    async def create_form(
        self,
        *,
        data: FormCreateRequest,
        db: Session,
        user: UUID
    ) -> FormInDB:
        new_form = Form(
            creator_id=user,
            title=data.title,
            description=data.description,
            fields=[field.model_dump() for field in data.fields]
        )

        db.add(new_form)
        db.commit()

        return FormInDB.model_validate(new_form)

    async def get_forms(
        self,
        *,
        db: Session,
        user: UUID
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

        return FormInDB.model_validate(form)

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
        user: UUID,
        db: Session,
        data: FormSubmissionCreate
    ) -> FormSubmissionResponse:
        form = db.query(Form).filter(Form.id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")

        submission = FormSubmission(
            form_id=form_id,
            user_id=user,
            data=[response.model_dump() for response in data.responses],
            submitted_at=str(datetime.now(timezone.utc))
        )

        db.add(submission)
        db.commit()

        return FormSubmissionResponse(
            id=UUID(str(submission.id)),
            message="Form submitted successfully"
        )
    
    def convert_to_dict(self, fields: list[FormFieldResponse]) -> dict:
        return {field.field_id: field.value for field in fields}

    async def get_submissions(
        self,
        *,
        form_id: UUID,
        page: int,
        limit: int,
        db: Session
    ) -> GetFormSubmissionsResponse:
        submissions = db.query(FormSubmission).filter(FormSubmission.form_id == form_id).limit(limit).offset((page - 1) * limit).all()
        total_count = len(submissions)

        submissions_data = [
            FormSubmissionDataForGetFormSubmissionResponse(
                submission_id=UUID(str(submission.id)),
                submitted_at=submission.submitted_at,  # type: ignore
                data=self.convert_to_dict(TypeAdapter(list[FormFieldResponse]).validate_python(submission.data))
            )
            for submission in submissions
        ]

        return GetFormSubmissionsResponse(
            total_count=total_count,
            page=page,
            limit=limit,
            submissions=submissions_data
        )

form_service = FormService()
