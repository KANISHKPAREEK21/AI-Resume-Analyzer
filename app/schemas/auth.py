from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict

class Token(BaseModel):
   access_token: str
   token_type: str = "bearer"


class TokenData(BaseModel):
   email: str | None = None


class LoginRequest(BaseModel):
   email: EmailStr
   password: str
