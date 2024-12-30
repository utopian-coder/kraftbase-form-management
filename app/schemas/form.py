from datetime import datetime
from email import message
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from uvicorn import Config


class FormField(BaseModel):
    field_id: str
    type: str | int | float | bool
    label: str
    required: bool

class FormBase(BaseModel):
    creator_id: UUID | None = Field(None, description="ID of the creator of the form")
    title: str | None = Field(None, description="Title of the form")
    description: str | None = Field(None, description="Description of the form")
    fields: list[FormField] | None = Field(None, description="Fields of the form")
    created_at: datetime | None = Field(None, description="Date and time the form was created")

class FormCreateRequest(FormBase):
    title: str
    description: str
    fields: list[FormField]

class FormCreate(FormBase):
    creator_id: UUID
    title: str
    description: str
    fields: list[FormField]

class FormInDB(FormBase):
    id: UUID
    creator_id: UUID
    title: str
    description: str
    fields: list[FormField]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FormFieldResponse(BaseModel):
    field_id: str
    value: str | int | float | bool

class FormSubmissionBase(BaseModel):
    form_id: UUID | None = Field(None, description="ID of the form")
    responses: list[FormFieldResponse] | None = Field(None, description="Data submitted in the form")
    submitted_at: str | None = Field(None, description="Date and time the form was submitted")

class FormSubmissionCreate(FormSubmissionBase):
    responses: list[FormFieldResponse]

class FormSubmissionInDB(FormSubmissionBase):
    id: UUID
    form_id: UUID
    data: list[FormFieldResponse]
    submitted_at: datetime

class FormSubmissionResponse(BaseModel):
    id: UUID
    message: str

class FormSubmissionDataForGetFormSubmissionResponse(BaseModel):
    submission_id: UUID
    submitted_at: datetime
    data: dict

    model_config = ConfigDict(from_attributes=True)

class GetFormSubmissionsResponse(BaseModel):
    total_count: int
    page: int
    limit: int
    submissions: list[FormSubmissionDataForGetFormSubmissionResponse]
