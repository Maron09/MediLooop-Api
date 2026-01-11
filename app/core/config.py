from pydantic_settings import BaseSettings
from pydantic import Field



class Settings(BaseSettings):
    """Application configuration settings."""
    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')
    API_V1_STR: str = Field(..., env='API_V1_STR')
    
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    REDIS_URL: str = Field(..., env='REDIS_URL')
    
    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')
    JWT_ALGORITHM: str = Field(..., env='JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')
    
    TOKEN_URL: str = Field(..., env='TOKEN_URL')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()