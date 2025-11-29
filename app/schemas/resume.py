from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from app.schemas.analysis import ResumeAnalysisRead

class ResumeBase(BaseModel):
   title: str
   resume_text: str
   target_role: Optional[str] = None
   job_description: Optional[str] = None

class ResumeCreate(ResumeBase):
   pass

class ResumeUpdate(BaseModel):
   title: Optional[str] = None
   resume_text: Optional[str] = None
   target_role: Optional[str] = None
   job_description: Optional[str] = None

class ResumeRead(BaseModel):
   id: int
   title: str
   resume_text: str
   target_role: Optional[str]
   job_description: Optional[str]
   created_at: datetime
   updated_at: datetime
   analyses: List[ResumeAnalysisRead] = Field(default_factory=list)

   model_config = SettingsConfigDict(from_attributes=True)
