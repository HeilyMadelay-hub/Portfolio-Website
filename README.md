# 🤖 Portfolio Chatbot con RAG

Un chatbot inteligente que responde preguntas sobre tu perfil profesional usando Google Gemini AI y técnicas de RAG (Retrieval-Augmented Generation).

## ✨ Características

- **🤖 IA Conversacional**: Powered by Google Gemini AI
- **📄 RAG Implementation**: Busca información en tus documentos personales
- **🎨 Interfaz Moderna**: Diseño responsive con animaciones fluidas
- **⚡ Tiempo Real**: Respuestas rápidas con indicador de escritura
- **📱 Responsive**: Funciona perfecto en desktop y móvil
- **🔒 Privacidad**: Tus documentos se procesan localmente

## 🛠️ Stack Tecnológico

### Frontend
- React 18
- Framer Motion (animaciones)
- Lucide React (iconos)
- CSS moderno con variables

### Backend
- Flask (Python)
- Google Gemini AI
- LangChain (RAG)
- ChromaDB (base de datos vectorial)
- PyPDF2 & python-docx (procesamiento de documentos)

## 🚀 Instalación y Configuración

### Prerrequisitos
- Node.js 16+ 
- Python 3.8+
- Google AI API Key ([Obtener aquí](https://makersuite.google.com/app/apikey))

### 1. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env y agrega tu GOOGLE_API_KEY
```

### 2. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# El frontend está configurado para usar proxy al puerto 5000
```

### 3. Agregar tus Documentos

Coloca tus documentos en `backend/app/data/documents/`:

```
backend/app/data/documents/
├── cv_actualizado.pdf
├── proyectos_portfolio.md
├── certificaciones.pdf
└── experiencia_laboral.docx
```

**Tipos de archivo soportados:**
- PDF (.pdf)
- Word (.docx) 
- Markdown (.md)
- Texto (.txt)

## 🏃‍♂️ Ejecutar el Proyecto

### Terminal 1 - Backend:
```bash
cd backend
python main.py
# Servidor corriendo en http://localhost:5000
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm start
# App corriendo en http://localhost:3000
```

## 📡 Endpoints de la API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/chat` | POST | Enviar mensaje al chatbot |
| `/api/chat/status` | GET | Estado del sistema RAG |
| `/api/chat/reload-documents` | POST | Recargar documentos |
| `/api/health` | GET | Health check |

### Ejemplo de uso:

```javascript
// Enviar mensaje
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "¿Qué experiencia tienes en React?"
  })
});

const data = await response.json();
console.log(data.response); // Respuesta del chatbot
```

## 🧠 Cómo Funciona el RAG

1. **Procesamiento**: Los documentos se dividen en chunks pequeños
2. **Embeddings**: Cada chunk se convierte en vectores usando Google AI
3. **Indexación**: Los vectores se guardan en ChromaDB
4. **Búsqueda**: Cuando preguntas algo, busca chunks relevantes
5. **Generación**: Gemini genera respuesta usando el contexto encontrado

```python
# Flujo interno simplificado
query = "¿Qué proyectos has desarrollado?"
relevant_docs = vectorstore.similarity_search(query, k=3)
context = "\\n".join([doc.content for doc in relevant_docs])
prompt = f"Contexto: {context}\\nPregunta: {query}"
response = gemini.generate(prompt)
```

## 📝 Tipos de Consultas Soportadas

### 📋 Información Profesional
- "¿Qué experiencia tienes?"
- "¿En qué empresas has trabajado?"
- "¿Cuántos años de experiencia tienes?"

### 🚀 Proyectos
- "¿Qué proyectos has desarrollado?"
- "Muéstrame tu trabajo más reciente"
- "¿Qué tecnologías usaste en [proyecto]?"

### 💻 Habilidades Técnicas
- "¿Qué lenguajes de programación manejas?"
- "¿Tienes experiencia con React?"
- "¿Qué frameworks conoces?"

### 🎓 Educación
- "¿Qué estudiaste?"
- "¿Tienes certificaciones?"
- "¿Dónde te formaste?"

### 📞 Contacto
- "¿Cómo puedo contactarte?"
- "¿Cuál es tu email?"
- "¿Estás disponible para trabajar?"

## ⚙️ Configuración Avanzada

### Ajustar Parámetros RAG

En `backend/app/config/settings.py`:

```python
# Tamaño de chunks para documentos
CHUNK_SIZE = 1000          # Caracteres por chunk
CHUNK_OVERLAP = 200        # Solapamiento entre chunks

# Número de documentos similares a buscar
SIMILARITY_TOP_K = 3       # Más documentos = más contexto
```

### Personalizar Prompts

En `backend/app/services/gemini_service.py`, modifica el método `_get_system_context()`:

```python
def _get_system_context(self):
    return """Eres un asistente especializado en [TU ÁREA].
    
    Personalidad:
    - [Describe tu personalidad profesional]
    - [Cómo quieres que responda]
    
    Especialidades:
    - [Tus áreas de expertise]
    """
```

## 🔧 Troubleshooting

### Problema: "GOOGLE_API_KEY not found"
**Solución**: Asegúrate de que `.env` existe y contiene tu API key

### Problema: ChromaDB errors
**Solución**: Elimina `backend/app/data/vectorstore/` y reinicia

### Problema: Documents not loading
**Solución**: Verifica que los archivos estén en `documents/` y usa `/api/chat/reload-documents`

### Problema: Frontend no conecta con Backend
**Solución**: Verifica que el backend esté en puerto 5000 y el proxy esté configurado

## 📦 Producción

### Docker (Recomendado)

```dockerfile
# Dockerfile para backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

```bash
# Build y deploy
docker build -t portfolio-chatbot-backend .
docker run -p 5000:5000 --env-file .env portfolio-chatbot-backend
```

### Deploy Manual

1. **Backend**: Sube a Heroku, Railway, o DigitalOcean
2. **Frontend**: Build y sube a Netlify, Vercel, o GitHub Pages

```bash
# Build frontend para producción
cd frontend
npm run build
# Sube la carpeta build/ a tu hosting
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección de Troubleshooting
2. Busca en Issues existentes
3. Crea un nuevo Issue con detalles del problema

---

**¡Happy Coding! 🚀**

*Hecho con ❤️ para desarrolladores que quieren destacar su portfolio*