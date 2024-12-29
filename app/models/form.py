from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Form(Base):
    __tablename__ = "form"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    title = Column(String)
    description = Column(String)
    fields = Column(JSON)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class FormSubmission(Base):
    __tablename__ = "form_submission"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    form_id = Column(UUID(as_uuid=True), ForeignKey("form.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    data = Column(JSON)

    submitted_at = Column(DateTime, default=datetime.now(timezone.utc))