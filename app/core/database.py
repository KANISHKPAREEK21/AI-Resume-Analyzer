from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings

settings = get_settings()

if settings.DATABASE_URL.startswith("sqlite"):
   engine: Engine = create_engine(
      settings.DATABASE_URL,
      connect_args={"check_same_thread": False},
      poolclass=StaticPool,
   )
else:
   engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
   pass

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()
