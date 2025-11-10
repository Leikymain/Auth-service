"""Servicio de gestión de tokens"""

from datetime import datetime, timedelta
from app.config import get_settings
from app.utils.password import generate_token

settings = get_settings()

class TokenService:
    @staticmethod
    def create_token_data(email: str) -> dict:
        """Crea datos de token nuevo"""
        return {
            "access_token": generate_token(),
            "requests_left": settings.initial_requests,
            "expires_at": (
                datetime.now(datetime.timezone.utc) + timedelta(days=settings.token_validity_days)
            ).isoformat()
        }
    
    @staticmethod
    def is_token_valid(expires_at: str, requests_left: int) -> tuple[bool, str]:
        """Verifica validez de token"""
        expires = datetime.fromisoformat(expires_at)
        
        if datetime.now(datetime.timezone.utc) > expires:
            return False, "Token expired"
        
        if requests_left <= 0:
            return False, "No requests left"
        
        return True, ""