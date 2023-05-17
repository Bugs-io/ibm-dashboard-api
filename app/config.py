import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANALYSIS_SERVICE_URL = os.getenv("ANALYSIS_SERVICE_URL")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_SECRET = os.getenv("JWT_SECRET")
    DB_PROVIDER = os.getenv("DB_PROVIDER")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_FILENAME = os.getenv("DB_FILENAME")
    DB_PROVIDER = os.getenv("DB_PROVIDER")
