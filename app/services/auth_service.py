"""Servicio de autenticación"""

from app.database import Database
from app.models.user import UserInDB
from app.utils.password import hash_password, verify_password, generate_secure_password
from app.services.email_service import EmailService
from app.services.token_service import TokenService
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    async def register_user(email: str) -> tuple[bool, str, str]:
        """
        Registra nuevo usuario.
        Returns: (success, message, password)
        """
        db = Database.get_database()
        
        # Verificar si existe
        existing = await db.users.find_one({"email": email})
        if existing:
            return False, "Email ya registrado", ""
        
        # Generar contraseña
        password = generate_secure_password(12)
        password_hash = hash_password(password)
        
        # Crear usuario
        user_data = {
            "email": email,
            "password_hash": password_hash,
            "access_token": None,
            "requests_left": 0,
            "expires_at": None,
            "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        }
        
        await db.users.insert_one(user_data)
        logger.info(f"Usuario creado: {email}")
        
        # Enviar email
        email_sent = await EmailService.send_password_email(email, password)
        
        return True, "Usuario creado", password
    
    @staticmethod
    async def login_user(email: str, password: str) -> tuple[bool, dict]:
        """
        Autentica usuario.
        Returns: (success, token_data)
        """
        db = Database.get_database()
        
        # Buscar usuario
        user = await db.users.find_one({"email": email})
        if not user or not verify_password(password, user["password_hash"]):
            return False, {}
        
        # Generar token
        token_data = TokenService.create_token_data(email)
        
        # Actualizar en DB
        await db.users.update_one(
            {"email": email},
            {"$set": token_data}
        )
        
        logger.info(f"Login exitoso: {email}")
        
        return True, token_data
    
    @staticmethod
    async def verify_token(token: str) -> tuple[bool, str]:
        """
        Verifica token y decrementa requests.
        Returns: (valid, error_message)
        """
        db = Database.get_database()
        
        user = await db.users.find_one({"access_token": token})
        if not user:
            return False, "Token not found"
        
        # Verificar validez
        valid, error = TokenService.is_token_valid(
            user["expires_at"],
            user["requests_left"]
        )
        
        if not valid:
            return False, error
        
        # Decrementar
        await db.users.update_one(
            {"access_token": token},
            {"$inc": {"requests_left": -1}}
        )
        
        return True, ""