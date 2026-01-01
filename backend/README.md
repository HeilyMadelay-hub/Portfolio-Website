# 🤖 Portfolio Chatbot - Sistema Híbrido RAG

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-009688.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**Un chatbot inteligente con arquitectura híbrida RAG para portfolio profesional**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [API](#-api) • [Arquitectura](#-arquitectura) • [Contribuir](#-contribuir)

</div>

---

## 📋 Descripción

Sistema de chatbot avanzado que implementa una arquitectura híbrida RAG (Retrieval-Augmented Generation) con flujo completo de procesamiento según el diagrama de arquitectura. Diseñado para responder preguntas sobre un portfolio profesional con alta precisión y seguridad.

## ✨ Características

### 🎯 Flujo Híbrido Completo
- **Rate Limiting** - Control de tráfico por cliente
- **Input Processing** - Validación y sanitización de entrada
- **Cache System** - Respuestas rápidas para consultas frecuentes
- **FAQ Classifier** - Detección automática de preguntas frecuentes
- **Section Validation** - Validación de contexto por sección
- **RAG Generation** - Generación aumentada con recuperación
- **Safety Checks** - Verificación de seguridad en entrada/salida
- **i18n Support** - Soporte multiidioma (ES, EN, FR, DE, IT, PT)

### 🚀 Tecnologías
- **LLM**: Google Gemini 1.5 Flash/Pro
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers
- **Cache**: Redis/Memory
- **Frameworks**: Flask & FastAPI
- **Monitoring**: Dashboard en tiempo real

## 📦 Instalación

### Requisitos Previos
- Python 3.11+
- Docker y Docker Compose (opcional)
- API Key de Google Gemini

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/chatbot-portfolio.git
cd chatbot-portfolio/backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tu configuración
```

5. **Inicializar la base de datos**
```bash
python scripts/populate_db.py populate
```

6. **Ejecutar la aplicación**
```bash
# Con Flask (default)
python main.py

# Con FastAPI
USE_FASTAPI=true python main.py
# o
python main.py fastapi
```

### Instalación con Docker

1. **Construir y ejecutar con Docker Compose**
```bash
docker-compose up -d
```

2. **Verificar estado**
```bash
docker-compose ps
docker-compose logs -f chatbot
```

3. **Inicializar base de datos**
```bash
docker-compose exec chatbot python scripts/populate_db.py populate
```

## 🎮 Uso

### Endpoints Principales

#### Chat Principal
```bash
POST /api/chat
Content-Type: application/json

{
    "message": "¿Cuál es tu experiencia profesional?",
    "language": "es",
    "context": "optional context"
}
```

#### Estado del Sistema
```bash
GET /api/chat/status
GET /api/chat/health
```

#### Dashboard de Monitoreo
```
http://localhost:5000/api/monitoring/dashboard
```

### Ejemplos de Uso

#### Python
```python
import requests

response = requests.post('http://localhost:5000/api/chat', 
    json={
        'message': '¿Qué proyectos has desarrollado?',
        'language': 'es'
    }
)

print(response.json())
```

#### cURL
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your experience", "language": "en"}'
```

## 🏗️ Arquitectura

### Diagrama de Flujo
```
Usuario → Rate Limiting → Input Processing → Cache Check
         ↓                                      ↓ (miss)
    [Blocked/429]                         Health Check
                                               ↓
                                        Section Validation
                                               ↓
                                         FAQ Classifier
                                          ↓ (no match)
                                      ChromaDB Search
                                               ↓
                                         Gemini LLM
                                               ↓
                                        Safety Check
                                               ↓
                                      i18n Translation
                                               ↓
                                          Response
```

### Componentes Principales

#### 1. **Orchestrator** (`app/core/orchestrator.py`)
- Coordina el flujo completo
- Gestiona el pipeline de procesamiento
- Maneja errores y fallbacks

#### 2. **Rate Limiter** (`app/utils/rate_limiter.py`)
- Control por IP/API Key/Usuario
- Configuración flexible por endpoint
- Estadísticas en tiempo real

#### 3. **FAQ Classifier** (`app/utils/faq_checker.py`)
- Clasificación ML de preguntas
- Respuestas pre-cacheadas
- Múltiples categorías

#### 4. **Safety Checker** (`app/services/safety_checker.py`)
- Validación de contenido
- Detección de PII
- Filtros de seguridad

#### 5. **Emergency Mode** (`app/services/emergency_mode.py`)
- Activación automática en fallos
- Respuestas de plantilla
- Auto-recuperación

## 📊 Monitoreo

### Dashboard Web
Accede al dashboard en: `http://localhost:5000/api/monitoring/dashboard`

Incluye:
- Estado de componentes en tiempo real
- Métricas de rendimiento
- Estadísticas de flujo
- Alertas del sistema

### Health Check
```bash
# Check único
python scripts/health_check.py

# Monitoreo continuo
python scripts/health_check.py --continuous --interval 30
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/unit/test_rate_limiter.py
pytest tests/integration/

# Con coverage
pytest --cov=app --cov-report=html
```

### Estructura de Tests
```
tests/
├── unit/           # Tests unitarios
├── integration/    # Tests de integración
└── e2e/           # Tests end-to-end
```

## 🔧 Configuración

### Variables de Entorno Principales

| Variable | Descripción | Default |
|----------|-------------|---------|
| `USE_FASTAPI` | Usar FastAPI en vez de Flask | `false` |
| `PORT` | Puerto del servidor | `5000` |
| `GOOGLE_API_KEY` | API Key de Gemini | Required |
| `RATE_LIMIT_ENABLED` | Activar rate limiting | `true` |
| `CACHE_ENABLED` | Activar sistema de cache | `true` |
| `DEBUG` | Modo debug | `false` |

Ver `.env.example` para lista completa.

## 📚 API Documentation

### Con FastAPI (Swagger)
```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/chat` | Enviar mensaje al chatbot |
| GET | `/api/chat/status` | Estado del sistema |
| GET | `/api/chat/health` | Health check |
| POST | `/api/chat/reload-documents` | Recargar documentos |
| GET | `/api/chat/languages` | Idiomas soportados |
| GET | `/api/monitoring/dashboard` | Dashboard HTML |
| GET | `/api/monitoring/metrics` | Métricas JSON |
| GET | `/api/monitoring/flow-stats` | Estadísticas de flujo |

## 🚀 Deployment

### Producción con Docker

1. **Configurar producción**
```bash
cp .env.example .env.production
# Editar con valores de producción
```

2. **Ejecutar con perfil de producción**
```bash
docker-compose --profile production up -d
```

3. **Con HTTPS (Nginx)**
```bash
# Configurar certificados SSL en ./ssl/
docker-compose --profile production up -d nginx
```

### Heroku
```bash
heroku create mi-chatbot-portfolio
heroku config:set GOOGLE_API_KEY=tu-api-key
git push heroku main
```

### Google Cloud Run
```bash
gcloud run deploy chatbot-portfolio \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## 🛠️ Scripts de Utilidad

### Gestión de Base de Datos
```bash
# Poblar base de datos
python scripts/populate_db.py populate

# Verificar documentos
python scripts/populate_db.py verify

# Limpiar base de datos
python scripts/populate_db.py clear

# Recargar documentos
python scripts/populate_db.py reload
```

### Health Check
```bash
# Check simple
python scripts/health_check.py

# Monitoreo continuo
python scripts/health_check.py --continuous
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Equipo

- **Tu Nombre** - *Desarrollo Principal* - [@tu-github](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Google Gemini API por el modelo LLM
- ChromaDB por la base de datos vectorial
- Comunidad open source

---

<div align="center">

**[⬆ Volver arriba](#-portfolio-chatbot---sistema-híbrido-rag)**

Hecho con ❤️ usando Python

</div>
