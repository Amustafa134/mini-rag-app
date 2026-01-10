from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    
    # Application configuration
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    # File handling configuration
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEfAULT_CHUNK_SIZE: int 
    
    # MongoDB configuration
    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
