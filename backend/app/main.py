from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Importar rutas
from app.routes import chat
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Crear app FastAPI
app = FastAPI(
    title="Portfolio Chatbot API",
    description="API para chatbot con IA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router, prefix="/api")

# Health check
@app.get("/api/health")
async def health():
    return {"status": "ok"}

# Inicializar ChromaDB al arrancar
@app.on_event("startup")
async def startup_event():
    try:
        from app.services.chromadb_service import chromadb_service
        chromadb_service.load_documents()
        logger.info("✅ ChromaDB inicializado")
    except Exception as e:
        logger.error(f"❌ Error inicializando ChromaDB: {e}")

# Para desarrollo directo
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
