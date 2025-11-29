from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
   get_password_hash,
   create_access_token,
   authenticate_user,
)
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.core.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
   existing = db.query(User).filter(User.email == user_in.email).first()
   if existing:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Email already registered.",
      )
   user = User(
      email=user_in.email,
      full_name=user_in.full_name,
      hashed_password=get_password_hash(user_in.password),
   )
   db.add(user)
   db.commit()
   db.refresh(user)
   return user


@router.post("/login", response_model=Token)
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
   user = authenticate_user(db, form_data.email, form_data.password)
   if not user:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Incorrect email or password.",
         headers={"WWW-Authenticate": "Bearer"},
      )
   access_token_expires = timedelta(
      minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
   )
   access_token = create_access_token(
      data={"sub": user.email},
      expires_delta=access_token_expires,
   )
   return Token(access_token=access_token)
