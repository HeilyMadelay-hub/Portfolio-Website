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
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    SIMILARITY_TOP_K = int(os.getenv('SIMILARITY_TOP_K', 3))
    
    # Gemini Configuration
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'models/embedding-001')
    
    # Application Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', "http://localhost:3000,http://127.0.0.1:3000").split(',')

    # --------------------- NUEVAS SECCIONES DE CONFIGURACIÓN ---------------------
    # Rate limiting defaults (pueden sobreescribirse vía env RATE_LIMIT_DEFAULTS en JSON)
    try:
        _rl_env = os.getenv('RATE_LIMIT_DEFAULTS')
        if _rl_env:
            import json as _json
            RATE_LIMIT_DEFAULTS = _json.loads(_rl_env)
        else:
            RATE_LIMIT_DEFAULTS = {
                'general': {'limit': 100, 'window': 3600},
                'chat': {'limit': 60, 'window': 3600},
                'chat_stream': {'limit': 30, 'window': 3600},
                'admin': {'limit': 10, 'window': 3600}
            }
    except Exception:
        RATE_LIMIT_DEFAULTS = {
            'general': {'limit': 100, 'window': 3600},
            'chat': {'limit': 60, 'window': 3600},
            'chat_stream': {'limit': 30, 'window': 3600},
            'admin': {'limit': 10, 'window': 3600}
        }

    # Cache backend and TTL
    CACHE_BACKEND = os.getenv('CACHE_BACKEND', 'memory')  # opciones: memory, redis, none
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # segundos por defecto

    # Monitoring endpoints / integration settings
    MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'False').lower() in ('1','true','yes')
    MONITORING_BACKEND = os.getenv('MONITORING_BACKEND', 'prometheus')  # prometheus, grafana, custom
    MONITORING_ENDPOINTS = {
        'metrics': os.getenv('MONITORING_METRICS_PATH', '/api/monitoring/metrics'),
        'dashboard': os.getenv('MONITORING_DASHBOARD_PATH', '/api/monitoring/dashboard'),
        'logs': os.getenv('MONITORING_LOGS_PATH', '/api/monitoring/logs')
    }

    # Docker / Environment overrides
    DOCKER_IMAGE = os.getenv('DOCKER_IMAGE', 'portfolio-backend:latest')
    DOCKER_CPU_LIMIT = os.getenv('DOCKER_CPU_LIMIT', None)
    DOCKER_MEMORY_LIMIT = os.getenv('DOCKER_MEMORY_LIMIT', None)

    # Otros ajustes operacionales
    MAX_PAYLOAD_BYTES = int(os.getenv('MAX_PAYLOAD_BYTES', 65536))
    ENABLE_DOC_RELOAD_ON_START = os.getenv('ENABLE_DOC_RELOAD_ON_START', 'False').lower() in ('1','true','yes')

    # Admin API keys (comma separated en env ADMIN_API_KEYS) para endpoints protegidos
    _admin_keys_env = os.getenv('ADMIN_API_KEYS', '')
    if _admin_keys_env:
        ADMIN_API_KEYS = [k.strip() for k in _admin_keys_env.split(',') if k.strip()]
    else:
        # Valor por defecto vacío — activar en entornos de producción
        ADMIN_API_KEYS = []

    ADMIN_API_KEY_REQUIRED = os.getenv('ADMIN_API_KEY_REQUIRED', 'True').lower() in ('1','true','yes')

    @classmethod
    def is_valid_admin_key(cls, key: str) -> bool:
        """Valida si la API key dada pertenece al conjunto de claves administrativas."""
        if not cls.ADMIN_API_KEY_REQUIRED:
            return True
        if not key:
            return False
        return key in cls.ADMIN_API_KEYS

    # ---------------- JWT / AUTH ----------------
    # Intentar leer JWT secret desde Docker secret file si existe, luego env var
    _jwt_secret = None
    _jwt_secret_file = os.getenv('JWT_SECRET_FILE', '/run/secrets/jwt_secret')
    try:
        if os.path.exists(_jwt_secret_file):
            with open(_jwt_secret_file, 'r') as f:
                _jwt_secret = f.read().strip()
    except Exception:
        _jwt_secret = None

    JWT_SECRET_KEY = _jwt_secret or os.getenv('JWT_SECRET_KEY', None)
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_MINUTES', 30))

    # ---------------- MONITORING ----------------
    PROMETHEUS_ENABLED = os.getenv('PROMETHEUS_ENABLED', 'False').lower() in ('1','true','yes')
    PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 9090))

    # ---------------- SECRETS / VAULT ----------------
    # Placeholder: configuración para integración con Vault (usar en producción)
    VAULT_ENABLED = os.getenv('VAULT_ENABLED', 'False').lower() in ('1','true','yes')
    VAULT_URL = os.getenv('VAULT_URL')
    VAULT_TOKEN = os.getenv('VAULT_TOKEN')

    @classmethod
    def validate_config(cls):
        """Valida que las configuraciones necesarias estén presentes y coherentes.
        - No exige GOOGLE_API_KEY (puede ser opcional según proveedor), pero advierte si falta.
        - Requiere GEMINI_MODEL y EMBEDDING_MODEL.
        - Verifica backend de cache válido.
        """
        errors = []
        warnings = []

        # Requerir modelos configurados
        if not cls.GEMINI_MODEL:
            errors.append('GEMINI_MODEL is required')
        if not cls.EMBEDDING_MODEL:
            errors.append('EMBEDDING_MODEL is required')

        # Cache backend valido
        if cls.CACHE_BACKEND not in ('memory', 'redis', 'none'):
            warnings.append(f"Unknown CACHE_BACKEND '{cls.CACHE_BACKEND}', falling back to 'memory'.")
            cls.CACHE_BACKEND = 'memory'

        # Rate limit defaults estructura
        if not isinstance(cls.RATE_LIMIT_DEFAULTS, dict):
            warnings.append('RATE_LIMIT_DEFAULTS has wrong format; using defaults')
            cls.RATE_LIMIT_DEFAULTS = {
                'general': {'limit': 100, 'window': 3600}
            }

        # GOOGLE_API_KEY es opcional (si se usan APIs externas puede ser necesario)
        if not cls.GOOGLE_API_KEY:
            warnings.append('GOOGLE_API_KEY not set; some external features may not work')

        # Monitoreo
        if cls.MONITORING_ENABLED and not cls.MONITORING_BACKEND:
            warnings.append('MONITORING_ENABLED is true but MONITORING_BACKEND is not configured')

        # Admin keys advertencia
        if cls.ADMIN_API_KEY_REQUIRED and not cls.ADMIN_API_KEYS:
            warnings.append('ADMIN_API_KEY_REQUIRED is True but ADMIN_API_KEYS is empty; admin endpoints will be inaccessible')

        # JWT secret
        if cls.ADMIN_API_KEY_REQUIRED and not cls.JWT_SECRET_KEY and not cls.ADMIN_API_KEYS:
            warnings.append('No JWT_SECRET_KEY ni ADMIN_API_KEYS configuradas; endpoints admin pueden estar protegidos insuficientemente')

        # Vault warnings
        if cls.VAULT_ENABLED and (not cls.VAULT_URL or not cls.VAULT_TOKEN):
            warnings.append('VAULT_ENABLED is true but VAULT_URL/VAULT_TOKEN no están configurados')

        if errors:
            raise ValueError('Configuration validation failed: ' + '; '.join(errors))

        # Retornar warnings en caso de querer emitirlos en logs
        return {'status': 'ok', 'warnings': warnings}

    @classmethod
    def as_dict(cls):
        """Devuelve un dict plano con la configuración útil para debugging/health endpoints"""
        return {
            'GEMINI_MODEL': cls.GEMINI_MODEL,
            'EMBEDDING_MODEL': cls.EMBEDDING_MODEL,
            'CACHE_BACKEND': cls.CACHE_BACKEND,
            'CACHE_TTL': cls.CACHE_TTL,
            'RATE_LIMIT_DEFAULTS': cls.RATE_LIMIT_DEFAULTS,
            'MONITORING': {
                'enabled': cls.MONITORING_ENABLED,
                'backend': cls.MONITORING_BACKEND,
                'endpoints': cls.MONITORING_ENDPOINTS
            },
            'DOCKER': {
                'image': cls.DOCKER_IMAGE,
                'cpu_limit': cls.DOCKER_CPU_LIMIT,
                'memory_limit': cls.DOCKER_MEMORY_LIMIT
            },
            'DEBUG': cls.DEBUG,
            'ADMIN_KEYS_CONFIGURED': bool(cls.ADMIN_API_KEYS),
            'ADMIN_API_KEY_REQUIRED': cls.ADMIN_API_KEY_REQUIRED
        }