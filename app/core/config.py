from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl


class Settings(BaseSettings):
   # App
   APP_NAME: str = "AI Resume Analyzer API"
   ENV: str = "development"

   # Database
   DATABASE_URL: str = "sqlite:///./app.db"

   # Mongo
   MONGO_URI: str = "mongodb://localhost:27017"
   MONGO_DB_NAME: str = "ai_resume_analyzer"

   # Security / JWT
   SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
   ALGORITHM: str = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

   # Azure OpenAI
   AZURE_OPENAI_ENDPOINT: AnyUrl | None = None
   AZURE_OPENAI_API_KEY: str | None = None
   AZURE_OPENAI_DEPLOYMENT: str | None = None
   AZURE_OPENAI_API_VERSION: str = "2024-05-01-preview"

   model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
