"""Configuración centralizada"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB
    mongodb_uri: str
    database_name: str = "authservice"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    
    # SMTP
    smtp_user: str
    smtp_password: str
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    
    # Token settings
    token_validity_days: int = 3
    initial_requests: int = 60
    
    # CORS
    allowed_origins: list = [
        "https://automapymes.com",
        "https://*.automapymes.com"
    ]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()