"""
Rate Limiting Middleware para FastAPI
Implementa rate limiting según el diagrama de flujo híbrido
"""

import logging
from functools import wraps
from typing import Callable, Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time

from ..utils.rate_limiter import check_rate_limit, get_client_identifier
from ..services.i18n_service import get_localized_message
from ..config.settings import Config

logger = logging.getLogger(__name__)

class RateLimitMiddleware:
    """
    Middleware para aplicar rate limiting a requests HTTP
    """
    
    def __init__(self, app, default_limit: int = 100, default_window: int = 3600):
        """
        Inicializa el middleware
        
        Args:
            app: Aplicación FastAPI
            default_limit: Límite default de requests
            default_window: Ventana de tiempo en segundos
        """
        self.app = app
        self.default_limit = default_limit
        self.default_window = default_window
        self.excluded_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/monitoring/status"
        ]
        
    async def __call__(self, request: Request, call_next):
        """
        Procesa el request aplicando rate limiting
        """
        # Excluir ciertas rutas del rate limiting
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Obtener identificador del cliente
        client_id = self._get_client_identifier(request)
        
        # Obtener configuración específica del endpoint
        endpoint_config = self._get_endpoint_config(request.url.path)
        
        # Verificar rate limit
        rate_result = check_rate_limit(
            client_id, 
            endpoint_config['category'],
            limit=endpoint_config.get('limit', self.default_limit),
            window=endpoint_config.get('window', self.default_window)
        )
        
        if not rate_result.get('allowed', False):
            # Detectar idioma del request
            language = request.headers.get('Accept-Language', 'es').split(',')[0][:2]
            
            # Crear respuesta de rate limit excedido
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": "rate_limit_exceeded",
                    "message": get_localized_message('rate_limit_exceeded', language),
                    "retry_after": rate_result.get('retry_after', 60),
                    "limit": rate_result.get('limit'),
                    "window": rate_result.get('window'),
                    "remaining": 0
                },
                headers={
                    "X-RateLimit-Limit": str(rate_result.get('limit', self.default_limit)),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + rate_result.get('retry_after', 60))),
                    "Retry-After": str(rate_result.get('retry_after', 60))
                }
            )
        
        # Procesar request
        response = await call_next(request)
        
        # Agregar headers de rate limiting a la respuesta
        response.headers["X-RateLimit-Limit"] = str(rate_result.get('limit', self.default_limit))
        response.headers["X-RateLimit-Remaining"] = str(rate_result.get('remaining', 0))
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + rate_result.get('window', self.default_window)))
        
        return response
    
    def _get_client_identifier(self, request: Request) -> str:
        """
        Obtiene identificador único del cliente
        Prioridad: API Key > User ID > Session ID > IP Address
        """
        # Verificar API Key
        api_key = request.headers.get('X-API-Key')
        if api_key:
            return f"api_key:{api_key}"
        
        # Verificar User ID (si existe autenticación)
        if hasattr(request.state, 'user_id'):
            return f"user:{request.state.user_id}"
        
        # Verificar Session ID
        session_id = request.cookies.get('session_id')
        if session_id:
            return f"session:{session_id}"
        
        # Usar IP como fallback
        client_ip = request.client.host if request.client else "unknown"
        
        # Verificar si viene de proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            client_ip = real_ip
        
        return f"ip:{client_ip}"
    
    def _get_endpoint_config(self, path: str) -> Dict[str, Any]:
        """
        Obtiene configuración de rate limiting específica del endpoint
        Ahora utiliza `Config.RATE_LIMIT_DEFAULTS` como fuente de verdad y permite
        sobrescribir límites por categoría.
        """
        # Mapeo base de rutas a categorías
        endpoint_configs = {
            "/api/chat": {"category": "chat"},
            "/api/chat/stream": {"category": "chat_stream"},
            "/api/suggest": {"category": "suggest"},
            "/api/search": {"category": "search"},
            "/api/documents": {"category": "documents"},
            "/api/admin": {"category": "admin"}
        }

        # Obtener defaults desde la configuración centralizada
        defaults = getattr(Config, 'RATE_LIMIT_DEFAULTS', {}) or {}

        # Enriquecer cada configuración con límites y ventanas
        for cfg in endpoint_configs.values():
            cat = cfg.get('category', 'general')
            cat_defaults = defaults.get(cat) or defaults.get('general') or {}
            cfg['limit'] = int(cat_defaults.get('limit', self.default_limit))
            cfg['window'] = int(cat_defaults.get('window', self.default_window))

        # Buscar configuración exacta
        if path in endpoint_configs:
            return endpoint_configs[path]

        # Buscar por prefijo
        for config_path, config in endpoint_configs.items():
            if path.startswith(config_path):
                return config

        # Configuración default basada en RATE_LIMIT_DEFAULTS.general
        general_default = defaults.get('general', {})
        return {
            "category": "general",
            "limit": int(general_default.get('limit', self.default_limit)),
            "window": int(general_default.get('window', self.default_window))
        }

def rate_limit_middleware(app, **kwargs):
    """
    Factory function para crear middleware de rate limiting
    """
    return RateLimitMiddleware(app, **kwargs)

def require_rate_limit(
    limit: int = 100,
    window: int = 3600,
    category: str = "general",
    key_func: Optional[Callable] = None
):
    """
    Decorator para aplicar rate limiting a endpoints específicos
    
    Args:
        limit: Número máximo de requests
        window: Ventana de tiempo en segundos
        category: Categoría del rate limiting
        key_func: Función opcional para generar key del cliente
    
    Ejemplo:
        @app.post("/api/chat")
        @require_rate_limit(limit=60, window=3600, category="chat")
        async def chat_endpoint(request: ChatRequest):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Obtener identificador del cliente
            if key_func:
                client_id = key_func(request)
            else:
                # Usar lógica default
                client_id = get_client_identifier(request)
            
            # Verificar rate limit
            rate_result = check_rate_limit(
                client_id, 
                category,
                limit=limit,
                window=window
            )
            
            if not rate_result.get('allowed', False):
                # Detectar idioma
                language = request.headers.get('Accept-Language', 'es').split(',')[0][:2]
                
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "rate_limit_exceeded",
                        "message": get_localized_message('rate_limit_exceeded', language),
                        "retry_after": rate_result.get('retry_after', 60),
                        "limit": limit,
                        "remaining": 0
                    },
                    headers={
                        "X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time() + rate_result.get('retry_after', 60))),
                        "Retry-After": str(rate_result.get('retry_after', 60))
                    }
                )
            
            # Agregar info de rate limiting al request
            request.state.rate_limit_info = rate_result
            
            # Ejecutar función original
            response = await func(request, *args, **kwargs)
            
            # Si la respuesta es un dict, agregar headers de rate limiting
            if isinstance(response, dict):
                response['rate_limit'] = {
                    'limit': limit,
                    'remaining': rate_result.get('remaining', 0),
                    'reset': int(time.time() + window)
                }
            
            return response
        
        return wrapper
    return decorator

# Configuración de rate limiting por tipo de cliente
RATE_LIMIT_CONFIGS = {
    'anonymous': {
        'chat': {'limit': 30, 'window': 3600},      # 30 chats/hora
        'suggest': {'limit': 50, 'window': 3600},   # 50 sugerencias/hora
        'search': {'limit': 100, 'window': 3600}    # 100 búsquedas/hora
    },
    'authenticated': {
        'chat': {'limit': 100, 'window': 3600},     # 100 chats/hora
        'suggest': {'limit': 200, 'window': 3600},  # 200 sugerencias/hora
        'search': {'limit': 500, 'window': 3600}    # 500 búsquedas/hora
    },
    'premium': {
        'chat': {'limit': 500, 'window': 3600},     # 500 chats/hora
        'suggest': {'limit': 1000, 'window': 3600}, # 1000 sugerencias/hora
        'search': {'limit': 2000, 'window': 3600}   # 2000 búsquedas/hora
    },
    'api_key': {
        'chat': {'limit': 1000, 'window': 3600},    # 1000 chats/hora
        'suggest': {'limit': 5000, 'window': 3600}, # 5000 sugerencias/hora
        'search': {'limit': 10000, 'window': 3600}  # 10000 búsquedas/hora
    }
}

def get_client_type(request: Request) -> str:
    """
    Determina el tipo de cliente basado en la autenticación
    """
    # Verificar API Key
    if request.headers.get('X-API-Key'):
        return 'api_key'
    
    # Verificar usuario autenticado
    if hasattr(request.state, 'user'):
        user = request.state.user
        if hasattr(user, 'is_premium') and user.is_premium:
            return 'premium'
        return 'authenticated'
    
    # Cliente anónimo
    return 'anonymous'

def get_rate_limit_config(request: Request, category: str) -> Dict[str, int]:
    """
    Obtiene configuración de rate limiting basada en el tipo de cliente
    """
    client_type = get_client_type(request)
    config = RATE_LIMIT_CONFIGS.get(client_type, RATE_LIMIT_CONFIGS['anonymous'])
    return config.get(category, {'limit': 100, 'window': 3600})
