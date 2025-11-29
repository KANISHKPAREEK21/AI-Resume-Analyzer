from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.mongo import get_mongo_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import ResumeAnalysis
from app.schemas.resume import ResumeCreate, ResumeRead, ResumeUpdate
from app.schemas.analysis import ResumeAnalysisRead
from app.services.ai_client import analyze_resume, AIAnalysisError

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
def create_resume(
   resume_in: ResumeCreate,
   db: Session = Depends(get_db),
   mongo_db=Depends(get_mongo_db),
   current_user: User = Depends(get_current_user),
):
   resume = Resume(
      user_id=current_user.id,
      title=resume_in.title,
      resume_text=resume_in.resume_text,
      target_role=resume_in.target_role,
      job_description=resume_in.job_description,
   )
   db.add(resume)
   db.commit()
   db.refresh(resume)

   # Store a copy in Mongo for unstructured logging
   mongo_db.resume_texts.insert_one(
      {
         "resume_id": resume.id,
         "user_id": current_user.id,
         "resume_text": resume.resume_text,
         "job_description": resume.job_description,
      }
   )

   return resume


@router.get("/", response_model=List[ResumeRead])
def list_resumes(
   db: Session = Depends(get_db),
   current_user: User = Depends(get_current_user),
):
   resumes = (
      db.query(Resume)
      .filter(Resume.user_id == current_user.id)
      .order_by(Resume.created_at.desc())
      .all()
   )
   return resumes


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(
   resume_id: int,
   db: Session = Depends(get_db),
   current_user: User = Depends(get_current_user),
):
   resume = (
      db.query(Resume)
      .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
      .first()
   )
   if not resume:
      raise HTTPException(status_code=404, detail="Resume not found.")
   return resume


@router.put("/{resume_id}", response_model=ResumeRead)
def update_resume(
   resume_id: int,
   resume_in: ResumeUpdate,
   db: Session = Depends(get_db),
   mongo_db=Depends(get_mongo_db),
   current_user: User = Depends(get_current_user),
):
   resume = (
      db.query(Resume)
      .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
      .first()
   )
   if not resume:
      raise HTTPException(status_code=404, detail="Resume not found.")

   for field, value in resume_in.model_dump(exclude_unset=True).items():
      setattr(resume, field, value)

   db.add(resume)
   db.commit()
   db.refresh(resume)

   # Update copy in Mongo
   mongo_db.resume_texts.update_one(
      {"resume_id": resume.id},
      {
         "$set": {
               "resume_text": resume.resume_text,
               "job_description": resume.job_description,
         }
      },
      upsert=True,
   )

   return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
   resume_id: int,
   db: Session = Depends(get_db),
   mongo_db=Depends(get_mongo_db),
   current_user: User = Depends(get_current_user),
):
   resume = (
      db.query(Resume)
      .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
      .first()
   )
   if not resume:
      raise HTTPException(status_code=404, detail="Resume not found.")

   db.delete(resume)
   db.commit()

   mongo_db.resume_texts.delete_many({"resume_id": resume_id})
   mongo_db.ai_logs.delete_many({"resume_id": resume_id})

   return


@router.post("/{resume_id}/analyze", response_model=ResumeAnalysisRead)
async def analyze_resume_endpoint(
   resume_id: int,
   db: Session = Depends(get_db),
   mongo_db=Depends(get_mongo_db),
   current_user: User = Depends(get_current_user),
):
   resume = (
      db.query(Resume)
      .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
      .first()
   )
   if not resume:
      raise HTTPException(status_code=404, detail="Resume not found.")

   try:
      result = await analyze_resume(resume.resume_text, resume.job_description)
      print("result", result)
   except AIAnalysisError as e:
      raise HTTPException(
         status_code=500,
         detail=f"AI analysis failed: {e}",
      )

   # Extract fields safely
   overall_score = result.get("overall_score")
   experience_summary = result.get("experience_summary")
   skills = result.get("skills", {})
   tech_skills = skills.get("technical", [])
   soft_skills = skills.get("soft", [])
   strengths = result.get("strengths", [])
   gaps = result.get("gaps", [])
   suggestions = result.get("improvement_suggestions", [])

   analysis = ResumeAnalysis(
      resume_id=resume.id,
      overall_score=overall_score,
      experience_summary=experience_summary,
      skills_technical=",".join(tech_skills),
      skills_soft=",".join(soft_skills),
      strengths="\n".join(strengths),
      gaps="\n".join(gaps),
      improvement_suggestions="\n".join(suggestions),
   )

   db.add(analysis)
   db.commit()
   db.refresh(analysis)

   # Log raw response to Mongo
   mongo_db.ai_logs.insert_one(
      {
         "resume_id": resume.id,
         "user_id": current_user.id,
         "raw_result": result,
      }
   )

   # Return proper ResumeAnalysisRead object
   return ResumeAnalysisRead(
         id=analysis.id,
         created_at=analysis.created_at,
         overall_score=analysis.overall_score,
         experience_summary=analysis.experience_summary,
         skills_technical=tech_skills,
         skills_soft=soft_skills,
         strengths=strengths,
         gaps=gaps,
         improvement_suggestions=suggestions,
      )



@router.get("/{resume_id}/analysis", response_model=list[ResumeAnalysisRead])
def list_analyses_for_resume(
   resume_id: int,
   db: Session = Depends(get_db),
   current_user: User = Depends(get_current_user),
):
   resume = (
      db.query(Resume)
      .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
      .first()
   )
   if not resume:
      raise HTTPException(status_code=404, detail="Resume not found.")

   analyses = (
      db.query(ResumeAnalysis)
      .filter(ResumeAnalysis.resume_id == resume_id)
      .order_by(ResumeAnalysis.created_at.desc())
      .all()
   )
   # SQLAlchemy → Pydantic conversion handled by from_attributes in schema
   return [
      ResumeAnalysisRead(
         id=a.id,
         created_at=a.created_at,
         overall_score=a.overall_score,
         experience_summary=a.experience_summary,
         skills_technical=a.skills_technical.split(",") if a.skills_technical else [],
         skills_soft=a.skills_soft.split(",") if a.skills_soft else [],
         strengths=a.strengths.split("\n") if a.strengths else [],
         gaps=a.gaps.split("\n") if a.gaps else [],
         improvement_suggestions=(
               a.improvement_suggestions.split("\n")
               if a.improvement_suggestions
               else []
         ),
      )
      for a in analyses
   ]
