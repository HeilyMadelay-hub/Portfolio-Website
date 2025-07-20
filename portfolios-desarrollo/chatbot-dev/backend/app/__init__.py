from flask import Flask
from flask_cors import CORS
from .config.settings import Config

def create_app():
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Validar configuración
    Config.validate_config()
    
    # Configurar CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Registrar blueprints
    from .routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    return app