"""
Application factory para el sistema híbrido de chatbot
Soporta tanto Flask como FastAPI
"""

import os
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app(config_name: Optional[str] = None):
    """
    Factory function para crear la aplicación
    Detecta automáticamente si usar Flask o FastAPI
    """
    
    # Detectar framework preferido
    use_fastapi = os.environ.get('USE_FASTAPI', 'false').lower() == 'true'
    
    if use_fastapi:
        return create_fastapi_app(config_name)
    else:
        return create_flask_app(config_name)

def create_fastapi_app(config_name: Optional[str] = None):
    """
    Crea aplicación FastAPI con todos los componentes del sistema híbrido
    """
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from contextlib import asynccontextmanager
    
    # Importar configuración
    from .config.settings import Config
    
    # Lifecycle manager para inicialización
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        logger.info("🚀 Iniciando sistema híbrido de chatbot...")
        
        # Inicializar componentes
        from .core.orchestrator import HybridRAGOrchestrator
        app.state.orchestrator = HybridRAGOrchestrator()
        
        logger.info("✅ Sistema híbrido inicializado correctamente")
        
        yield
        
        # Shutdown
        logger.info("🛑 Apagando sistema híbrido...")
    
    # Crear aplicación FastAPI
    app = FastAPI(
        title="Portfolio Chatbot Hybrid API",
        description="Sistema híbrido RAG con flujo completo del diagrama",
        version="2.0.0",
        lifespan=lifespan
    )
    
    # Configurar CORS
    from .middleware.cors_middleware import setup_cors
    app = setup_cors(app)
    
    # Agregar middleware de rate limiting
    from .middleware.rate_limit_middleware import RateLimitMiddleware
    app.add_middleware(RateLimitMiddleware)

    # Agregar middleware de logging estructurado
    from .middleware.logging_middleware import StructuredLoggingMiddleware, register_flask_logging
    try:
        app.add_middleware(StructuredLoggingMiddleware)
    except Exception:
        # Flask: registrar handlers
        register_flask_logging(app)
    
    # Registrar routers
    from .routes import chat_router, monitoring_router
    app.include_router(chat_router)
    app.include_router(monitoring_router)
    
    # Health check root
    @app.get("/")
    async def root():
        return {
            "service": "Portfolio Chatbot Hybrid API",
            "version": "2.0.0",
            "status": "operational",
            "framework": "FastAPI",
            "diagram_implementation": "complete",
            "endpoints": {
                "chat": "/api/chat",
                "status": "/api/chat/status",
                "health": "/api/chat/health",
                "monitoring": "/api/monitoring/dashboard",
                "metrics": "/api/monitoring/metrics",
                "docs": "/docs"
            }
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "framework": "FastAPI"}
    
    logger.info("✅ FastAPI app created successfully")
    return app

def create_flask_app(config_name: Optional[str] = None):
    """
    Crea aplicación Flask con todos los componentes del sistema híbrido
    """
    from flask import Flask, jsonify
    from flask_cors import CORS
    
    # Importar configuración
    from .config.settings import Config
    
    # Crear aplicación Flask
    app = Flask(__name__)
    
    # Cargar configuración
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
    elif config_name == 'production':
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = Config.DEBUG
    
    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-API-Key"]
        }
    })
    
    # Registrar blueprints
    from .routes import chat_router, monitoring_router
    app.register_blueprint(chat_router)
    app.register_blueprint(monitoring_router)
    
    # Inicializar componentes
    with app.app_context():
        from .core.orchestrator import HybridRAGOrchestrator
        app.orchestrator = HybridRAGOrchestrator()
        logger.info("✅ Sistema híbrido inicializado en Flask")
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            "service": "Portfolio Chatbot Hybrid API",
            "version": "2.0.0",
            "status": "operational",
            "framework": "Flask",
            "diagram_implementation": "complete",
            "endpoints": {
                "chat": "/api/chat",
                "status": "/api/chat/status",
                "health": "/api/chat/health",
                "monitoring": "/api/monitoring/dashboard",
                "metrics": "/api/monitoring/metrics"
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "framework": "Flask"})
    
    # Manejo de errores global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    logger.info("✅ Flask app created successfully")
    return app

# Función de utilidad para obtener la aplicación
def get_app():
    """
    Obtiene la instancia de la aplicación
    """
    use_fastapi = os.environ.get('USE_FASTAPI', 'false').lower() == 'true'
    
    if use_fastapi:
        logger.info("Using FastAPI framework")
    else:
        logger.info("Using Flask framework")
    
    return create_app()

# Exportar funciones principales
__all__ = ['create_app', 'create_fastapi_app', 'create_flask_app', 'get_app']
