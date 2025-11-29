from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.user import User

settings = get_settings()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
   return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
   # Truncate to bcrypt 72-byte limit (safe for all passwords)
   return pwd_context.hash(password[:72])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
   to_encode = data.copy()
   expire = datetime.now(timezone.utc) + (
      expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   )
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(
      to_encode,
      settings.SECRET_KEY,
      algorithm=settings.ALGORITHM,
   )
   return encoded_jwt


def get_user_by_email(db: Session, email: str) -> Optional[User]:
   return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
   user = get_user_by_email(db, email)
   if not user:
      return None
   if not verify_password(password, user.hashed_password):
      return None
   return user


async def get_current_user(
   credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
   token = credentials.credentials
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials.",
      headers={"WWW-Authenticate": "Bearer"},
   )
   try:
      payload = jwt.decode(
         token,
         settings.SECRET_KEY,
         algorithms=[settings.ALGORITHM],
      )
      email: str | None = payload.get("sub")
      if email is None:
         raise credentials_exception
   except JWTError:
      raise credentials_exception

   user = get_user_by_email(db, email=email)
   if user is None:
      raise credentials_exception
   return user
