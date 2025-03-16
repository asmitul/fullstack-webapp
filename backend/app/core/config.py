import os
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    API_V1_STR: str = "/api/v1"
    
    # JWT Settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_jwt_secret_key_change_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # MongoDB Settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/taskmanager")
    
    # Redis Settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    VPS_HOST: str = os.getenv("VPS_HOST", "localhost")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        f"http://{VPS_HOST}",
        f"http://{VPS_HOST}:3000",
        f"http://{VPS_HOST}:8000",
    ]
    
    class Config:
        case_sensitive = True

settings = Settings() 