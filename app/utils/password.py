"""Utilidades para passwords"""

import bcrypt
import secrets

def generate_secure_password(length: int = 12) -> str:
    """Genera contraseña aleatoria segura"""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password: str) -> str:
    """Hashea password con bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica password contra hash"""
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def generate_token() -> str:
    """Genera token seguro"""
    return secrets.token_urlsafe(32)