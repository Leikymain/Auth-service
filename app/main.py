"""FastAPI app principal"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import Database
from app.routes import auth
from app.utils.logger import setup_logger
from datetime import datetime, timezone
import os

# Setup
settings = get_settings()
logger = setup_logger()

# App
@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    logger.info("AuthService iniciado")
    try:
        yield
    finally:
        await Database.disconnect()
        logger.info("AuthService detenido")


app = FastAPI(
    title="AuthService",
    description="Sistema centralizado de autenticación",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins + [
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)

# Root
@app.get("/")
def root():
    return {
        "service": "AuthService",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health():
    try:
        db = Database.get_database()
        await db.command('ping')
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.now(datetime.timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)