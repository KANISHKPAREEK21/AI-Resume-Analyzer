from datetime import datetime
from pydantic import BaseModel, field_validator
from pydantic_settings import SettingsConfigDict

class ResumeAnalysisBase(BaseModel):
   overall_score: int | None = None
   experience_summary: str | None = None
   skills_technical: list[str] | None = None
   skills_soft: list[str] | None = None
   strengths: list[str] | None = None
   gaps: list[str] | None = None
   improvement_suggestions: list[str] | None = None

   # Convert comma-separated strings from the DB to lists
   @field_validator("skills_technical", "skills_soft", mode="before")
   @classmethod
   def _ensure_list_comma(cls, v):
      if v is None:
         return []
      if isinstance(v, str):
         return [item.strip() for item in v.split(",") if item.strip()]
      return v  # already a list or something else

   # Convert newline-separated strings from the DB to lists
   @field_validator("strengths", "gaps", "improvement_suggestions", mode="before")
   @classmethod
   def _ensure_list_newline(cls, v):
      if v is None:
         return []
      if isinstance(v, str):
         return [line.strip() for line in v.split("\n") if line.strip()]
      return v


class ResumeAnalysisRead(ResumeAnalysisBase):
   id: int
   created_at: datetime

   model_config = SettingsConfigDict(from_attributes=True)
