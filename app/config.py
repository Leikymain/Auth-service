from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB
    mongodb_uri: str
    database_name: str

    # JWT / Seguridad
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24 * 3  # 3 días

    # Email
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_server: str | None = None
    smtp_port: int | None = None

    # Resend API
    resend_api_key: str | None = None  

    # App
    environment: str = "production"
    app_name: str = "AuthService"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Carga las variables de entorno con caché"""
    return Settings()
