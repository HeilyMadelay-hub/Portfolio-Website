"""
Routes module for the hybrid chatbot application
"""

# Importar routers según el framework disponible
try:
    # FastAPI imports
    from .chat import router as chat_router
    from .monitoring import router as monitoring_router
    
    # Exportar routers FastAPI
    __all__ = ['chat_router', 'monitoring_router']
    
except ImportError:
    # Flask imports (fallback)
    from .chat import chat_bp as chat_router
    from .monitoring import monitoring_bp as monitoring_router
    
    # Exportar blueprints Flask
    __all__ = ['chat_router', 'monitoring_router']
