from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True, index=True, nullable=False)
   full_name = Column(String, nullable=True)
   hashed_password = Column(String, nullable=False)
   created_at = Column(
      DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
   )

   resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")
