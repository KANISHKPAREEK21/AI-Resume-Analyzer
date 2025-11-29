from pymongo import MongoClient
from app.core.config import get_settings

settings = get_settings()

mongo_client = MongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]

def get_mongo_db():
    try:
        yield mongo_db
    finally:
        pass  # Mongo connections are safe to reuse
