from datetime import datetime, timezone
from sqlalchemy import (
   Column,
   Integer,
   String,
   Text,
   DateTime,
   ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Resume(Base):
   __tablename__ = "resumes"

   id = Column(Integer, primary_key=True, index=True)
   user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
   title = Column(String, nullable=False)
   resume_text = Column(Text, nullable=False)
   target_role = Column(String, nullable=True)
   job_description = Column(Text, nullable=True)
   created_at = Column(
      DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
   )
   updated_at = Column(
      DateTime(timezone=True),
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc),
   )

   owner = relationship("User", back_populates="resumes")
   analyses = relationship(
      "ResumeAnalysis",
      back_populates="resume",
      cascade="all, delete-orphan",
   )
