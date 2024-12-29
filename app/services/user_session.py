import base64
from typing import Annotated
from uuid import uuid4

from fastapi import Cookie, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import db
from app.models.session import UserSession
from app.models.user import User
from app.schemas.auth import UserInDB


class SessionCookies(BaseModel):
  session_token: str


class UserSessionService:
  @staticmethod
  async def create(user: User, db: Session) -> str:
    session_token = uuid4()
    user_session = UserSession(token=session_token, user=user.id)  

    db.add(user_session)
    db.commit()

    return base64.urlsafe_b64encode(session_token)

  @staticmethod
  async def authorize(cookies: Annotated[SessionCookies, Cookie()], db = Depends(db.get_db)) -> User:
    session_token = cookies.session_token
    _token = base64.urlsafe_b64decode(session_token)

    # Retrieve user
    user_session = db.query(UserSession).filter(UserSession.token == _token).first()
    
    if user_session:
        return UserInDB.model_validate(user_session.user)
    else:
        raise HTTPException(status_code=401, detail="Invalid session or user not found")

  @staticmethod
  async def logout(cookies: Annotated[SessionCookies, Cookie()], db = Depends(db.get_db)):
    session_token = cookies.session_token
    _token = base64.urlsafe_b64decode(session_token)

    # Delete the user's session_token in the database
    db.query(UserSession).filter(UserSession.token == _token).delete()
