from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from typing import Optional

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
    
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str
    
    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None
    
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str = None
    
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
