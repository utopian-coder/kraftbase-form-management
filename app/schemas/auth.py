from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
  
class UserLogin(UserBase):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: int
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    message: str
    session_token: str
