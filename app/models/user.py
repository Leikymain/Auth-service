"""Modelos Pydantic para User"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserInDB(BaseModel):
    email: EmailStr
    password_hash: str
    access_token: Optional[str] = None
    requests_left: int = 0
    expires_at: Optional[str] = None
    created_at: str

class RegisterRequest(BaseModel):
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class VerifyTokenRequest(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    requests_available: int
    expires_in_days: int

class StatsResponse(BaseModel):
    email: str
    requests_left: int
    expires_at: str

class VerifyResponse(BaseModel):
    valid: bool
    detail: Optional[str] = None
