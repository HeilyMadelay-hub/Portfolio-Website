"""
CORS Middleware Configuration
Configura CORS para el chatbot híbrido
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

def setup_cors(
    app: FastAPI,
    allowed_origins: Optional[List[str]] = None,
    allow_credentials: bool = True,
    allow_methods: Optional[List[str]] = None,
    allow_headers: Optional[List[str]] = None
):
    """
    Configura CORS middleware para la aplicación
    
    Args:
        app: Instancia de FastAPI
        allowed_origins: Lista de orígenes permitidos
        allow_credentials: Permitir credenciales
        allow_methods: Métodos HTTP permitidos
        allow_headers: Headers permitidos
    """
    
    # Orígenes default
    if allowed_origins is None:
        allowed_origins = [
            "http://localhost:3000",      # Frontend desarrollo React
            "http://localhost:5173",      # Frontend desarrollo Vite
            "http://localhost:8080",      # Frontend desarrollo Vue
            "http://localhost:4200",      # Frontend desarrollo Angular
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8080",
            "http://127.0.0.1:4200",
            "https://tu-dominio.com",     # Producción
            "https://www.tu-dominio.com"
        ]
    
    # Métodos default
    if allow_methods is None:
        allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    
    # Headers default
    if allow_headers is None:
        allow_headers = [
            "Content-Type",
            "Authorization",
            "X-API-Key",
            "X-Request-ID",
            "Accept-Language",
            "X-Session-ID",
            "X-Client-Version"
        ]
    
    # Agregar middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        expose_headers=[
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining", 
            "X-RateLimit-Reset",
            "X-Request-ID",
            "X-Response-Time"
        ]
    )
    
    return app

def get_cors_config():
    """
    Obtiene configuración CORS desde variables de entorno
    """
    import os
    
    # Leer configuración del entorno
    cors_origins = os.getenv("CORS_ORIGINS", "").split(",")
    cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
    
    # Si no hay orígenes configurados, usar defaults
    if not cors_origins:
        cors_origins = None
    
    return {
        "allowed_origins": cors_origins,
        "allow_credentials": os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true",
        "allow_methods": os.getenv("CORS_ALLOW_METHODS", "").split(",") or None,
        "allow_headers": os.getenv("CORS_ALLOW_HEADERS", "").split(",") or None
    }
