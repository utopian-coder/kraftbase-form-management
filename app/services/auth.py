from argon2 import PasswordHasher
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_session import UserSessionService
from app.schemas.auth import LoginResponse, RegisterResponse, UserCreate, UserInDB, UserLogin


class AuthService:
  password_hasher = PasswordHasher()

  async def register(
    self,
    *,
    data: UserCreate,
    db: Session
  ) -> dict:
    hashed_password = self.password_hasher.hash(data.password)

    new_user=User(
      username=data.username,
      email=data.email,
      password=hashed_password
    )

    db.add(new_user)
    db.commit()


    return {
      "user": RegisterResponse.model_validate(new_user),
      "session_token": await UserSessionService.create(user=new_user, db=db)
    }

  async def login(
    self,
    *,
    data: UserLogin,
    db: Session
  ) -> LoginResponse:
    user_db_obj = db.query(User).filter(User.email == data.email).first()
    user_obj = UserInDB.model_validate(user_db_obj)

    if not user_obj or not user_obj.password or not self.password_hasher.verify(user_obj.password, data.password):
      raise HTTPException(status_code=400, detail="Incorrect email or password")

    session_token = await UserSessionService.create(user=user_db_obj, db=db)
    
    return LoginResponse(message="Login successful", session_token=session_token)


auth_service = AuthService()
