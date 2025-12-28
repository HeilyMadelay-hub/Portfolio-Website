"""
Main entry point para el sistema híbrido de chatbot
Soporta tanto Flask como FastAPI
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def run_flask():
    """Ejecuta la aplicación con Flask"""
    from app import create_flask_app
    
    app = create_flask_app()
    
    # Configuración del servidor
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"🚀 Starting Flask server on {host}:{port}")
    logger.info(f"📊 Dashboard available at http://{host}:{port}/api/monitoring/dashboard")
    logger.info(f"💬 Chat endpoint at http://{host}:{port}/api/chat")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )

def run_fastapi():
    """Ejecuta la aplicación con FastAPI usando Uvicorn"""
    try:
        import uvicorn
    except ImportError:
        logger.error("Uvicorn no está instalado. Instálalo con: pip install uvicorn")
        sys.exit(1)
    
    # Configuración del servidor
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    reload = os.environ.get('DEBUG', 'True').lower() == 'true'
    workers = int(os.environ.get('WORKERS', 1))
    
    logger.info(f"🚀 Starting FastAPI server on {host}:{port}")
    logger.info(f"📚 API Docs available at http://{host}:{port}/docs")
    logger.info(f"📊 Dashboard available at http://{host}:{port}/api/monitoring/dashboard")
    logger.info(f"💬 Chat endpoint at http://{host}:{port}/api/chat")
    
    uvicorn.run(
        "app:create_fastapi_app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
        log_level="info"
    )

def main():
    """
    Punto de entrada principal
    Detecta qué framework usar basado en variables de entorno
    """
    
    # Imprimir banner
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🤖 PORTFOLIO CHATBOT - SISTEMA HÍBRIDO RAG 🤖      ║
    ║                                                          ║
    ║     Implementación completa del diagrama de flujo:      ║
    ║     Rate Limiting → Processing → RAG → Response         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Detectar framework
    use_fastapi = os.environ.get('USE_FASTAPI', 'false').lower() == 'true'
    
    # También se puede forzar con argumento de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == 'fastapi':
            use_fastapi = True
        elif sys.argv[1] == 'flask':
            use_fastapi = False
    
    # Ejecutar servidor apropiado
    if use_fastapi:
        logger.info("🚀 Starting with FastAPI framework")
        run_fastapi()
    else:
        logger.info("🚀 Starting with Flask framework")
        run_flask()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
