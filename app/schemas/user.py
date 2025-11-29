from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict

class UserBase(BaseModel):
   email: EmailStr
   full_name: str | None = None

class UserCreate(UserBase):
   password: str

class UserRead(UserBase):
   id: int
   created_at: datetime

   model_config = SettingsConfigDict(from_attributes=True)
