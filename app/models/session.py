from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserSession(Base):
    __tablename__ = "user_session"

    token = Column(UUID(as_uuid=True), primary_key=True)
    user = Column(UUID(as_uuid=True), ForeignKey("user.id"))
