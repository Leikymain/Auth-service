"""Gestión de conexión a MongoDB"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect(cls):
        """Conecta a MongoDB"""
        cls.client = AsyncIOMotorClient(settings.mongodb_uri)
        logger.info("Conectado a MongoDB Atlas")
        
        # Crear índices
        db = cls.client[settings.database_name]
        await db.users.create_index("email", unique=True)
        await db.users.create_index("access_token")
        logger.info("Índices creados")
    
    @classmethod
    async def disconnect(cls):
        """Cierra conexión"""
        if cls.client:
            cls.client.close()
            logger.info("Conexión a MongoDB cerrada")
    
    @classmethod
    def get_database(cls):
        """Obtiene la instancia de la base de datos"""
        return cls.client[settings.database_name]