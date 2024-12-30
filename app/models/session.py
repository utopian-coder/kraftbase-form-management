from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base


class UserSession(Base):
    __tablename__ = "user_session"

    token = Column(UUID(as_uuid=True), primary_key=True)
    user = Column(UUID(as_uuid=True), ForeignKey("user.id"))
