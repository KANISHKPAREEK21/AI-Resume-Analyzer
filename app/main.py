from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine  
from app.core.config import get_settings
from app.routes import auth, resumes

settings = get_settings()

# Create tables 
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# CORS – can be adjust origins for frontend later
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(resumes.router)
