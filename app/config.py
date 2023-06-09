import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANALYSIS_SERVICE_URL = os.getenv("ANALYSIS_SERVICE_URL")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    CLIENT_URL = os.getenv("CLIENT_URL")
    CLIENT_URL_LOCAL = os.getenv("CLIENT_URL_LOCAL")
    CLIENT_URL_REGEX = os.getenv("CLIENT_URL_REGEX")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_SECRET = os.getenv("JWT_SECRET")
    DB_PROVIDER = os.getenv("DB_PROVIDER")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_FILENAME = os.getenv("DB_FILENAME")
    DB_PROVIDER = os.getenv("DB_PROVIDER")
    TESTING = os.getenv("TESTING", 'False').lower() in ('true', '1', 't')
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
