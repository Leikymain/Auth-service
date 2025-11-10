"""Configuración de logging"""

import logging
import sys

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