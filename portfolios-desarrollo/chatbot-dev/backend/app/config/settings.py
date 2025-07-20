import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base para el chatbot"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'app', 'data')
    DOCUMENTS_DIR = os.path.join(DATA_DIR, 'documents')
    VECTORSTORE_DIR = os.path.join(DATA_DIR, 'vectorstore')
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    SIMILARITY_TOP_K = 3
    
    # Gemini Configuration
    GEMINI_MODEL = 'gemini-pro'
    EMBEDDING_MODEL = 'models/embedding-001'
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    @classmethod
    def validate_config(cls):
        """Valida que todas las configuraciones necesarias estén presentes"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required. Set it in your .env file")
        return True