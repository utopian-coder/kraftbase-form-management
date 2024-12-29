from argon2 import PasswordHasher
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_session import UserSessionService
from app.schemas.auth import LoginResponse, UserCreate, UserInDB, UserLogin


class AuthService:
  password_hasher = PasswordHasher()

  async def register(
    self,
    *,
    data: UserCreate,
    db: Session
  ) -> UserInDB:
    hashed_password = self.password_hasher.hash(data.password)

    new_user=User(
      username=data.username,
      email=data.email,
      password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return UserInDB.model_validate(new_user)

  async def login(
    self,
    *,
    data: UserLogin,
    db: Session
  ) -> LoginResponse:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not self.password_hasher.verify(UserInDB.model_validate(user).password, data.password):
      raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    session_token = await UserSessionService.create(user=user, db=db)
    
    return LoginResponse(message="Login successful", session_token=session_token)


auth_service = AuthService()
