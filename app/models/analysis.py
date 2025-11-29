from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ResumeAnalysis(Base):
   __tablename__ = "resume_analyses"

   id = Column(Integer, primary_key=True, index=True)
   resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"))
   overall_score = Column(Integer, nullable=True)
   experience_summary = Column(Text, nullable=True)
   skills_technical = Column(Text, nullable=True)  # store as comma-separated or JSON
   skills_soft = Column(Text, nullable=True)
   strengths = Column(Text, nullable=True)
   gaps = Column(Text, nullable=True)
   improvement_suggestions = Column(Text, nullable=True)
   created_at = Column(
      DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
   )

   resume = relationship("Resume", back_populates="analyses")
