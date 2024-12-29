from pydantic import BaseModel, Field


class FormField(BaseModel):
    name: str
    type: str | int | float | bool
    label: str
    required: bool

class FormBase(BaseModel):
    creator_id: str | None = Field(None, description="ID of the creator of the form")
    title: str | None = Field(None, description="Title of the form")
    description: str | None = Field(None, description="Description of the form")
    fields: list[FormField] | None = Field(None, description="Fields of the form")
    created_at: str | None = Field(None, description="Date and time the form was created")

class FormCreate(FormBase):
    creator_id: str
    title: str
    description: str
    fields: list[FormField]

class FormInDB(FormBase):
    id: str
    creator_id: str
    title: str
    description: str
    fields: list[FormField]
    created_at: str
    
class FormSubmissionBase(BaseModel):
    form_id: str | None = Field(None, description="ID of the form")
    data: dict | None = Field(None, description="Data submitted in the form")
    submitted_at: str | None = Field(None, description="Date and time the form was submitted")

class FormSubmissionCreate(FormSubmissionBase):
    data: dict

class FormSubmissionInDB(FormSubmissionBase):
    id: str
    form_id: str
    data: dict
    submitted_at: str
