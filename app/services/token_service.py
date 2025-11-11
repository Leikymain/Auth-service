"""Servicio de gestión de tokens"""

from datetime import datetime, timedelta, timezone
from app.config import get_settings
from app.utils.password import generate_token
import pytz

settings = get_settings()
spain_tz = pytz.timezone("Europe/Madrid")

class TokenService:
    @staticmethod
    def create_token_data(email: str) -> dict:
        """Crea datos de token nuevo"""
        return {
            "access_token": generate_token(),
            "requests_left": settings.initial_requests,
            "expires_at": (
                datetime.now(spain_tz).replace(microsecond=0) + timedelta(days=settings.token_validity_days)
            ).replace(microsecond=0).isoformat()
        }
    
    @staticmethod
    def is_token_valid(expires_at: str, requests_left: int) -> tuple[bool, str]:
        """Verifica validez de token"""
        expires = datetime.fromisoformat(expires_at)
        
        if datetime.now(spain_tz).replace(microsecond=0) > expires:
            return False, "Token expired"
        
        if requests_left <= 0:
            return False, "No requests left"
        
        return True, ""