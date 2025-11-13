"""Configuración de logging"""
from datetime import datetime, timezone
from app.database import Database
import pytz
import logging
import sys

spain_tz = pytz.timezone("Europe/Madrid")
def setup_logger(name: str = "authservice") -> logging.Logger:
    """Configura logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Handler para consola
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

async def log_event(event_type: str, email: str, metadata: dict = None):
    """Guarda un evento (registro, login, etc.) en la colección logs."""
    db = Database.get_database()
    await db["logs"].insert_one({
        "event": event_type,
        "email": email,
        "timestamp": datetime.now(spain_tz).replace(microsecond=0).isoformat(),
        "metadata": metadata or {}
    })