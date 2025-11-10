"""Endpoints de autenticación"""

from fastapi import APIRouter, HTTPException, status
from app.models.user import *
from app.services.auth_service import AuthService
from app.database import Database
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(request: RegisterRequest):
    """Registra nuevo usuario"""
    email = request.email.lower()
    
    success, message, password = await AuthService.register_user(email)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )
    
    return {
        "detail": "Contraseña enviada por correo electrónico",
        "email": email
    }

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login y generación de token"""
    email = request.email.lower()
    
    success, token_data = await AuthService.login_user(email, request.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    from app.config import get_settings
    settings = get_settings()
    
    return TokenResponse(
        access_token=token_data["access_token"],
        requests_available=token_data["requests_left"],
        expires_in_days=settings.token_validity_days
    )

@router.post("/verify-token", response_model=VerifyResponse)
async def verify_token(request: VerifyTokenRequest):
    """Verifica token"""
    valid, error = await AuthService.verify_token(request.token)
    
    if not valid:
        return VerifyResponse(valid=False, detail=error)
    
    return VerifyResponse(valid=True)

@router.get("/stats", response_model=StatsResponse)
async def get_stats(token: str):
    """Estadísticas del token"""
    db = Database.get_database()
    user = await db.users.find_one({"access_token": token})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )
    
    return StatsResponse(
        email=user["email"],
        requests_left=user["requests_left"],
        expires_at=user["expires_at"]
    )
