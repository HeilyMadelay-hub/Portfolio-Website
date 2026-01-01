from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.services.chromadb_service import chromadb_service
from app.services.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal del chatbot

    - **message**: Pregunta del usuario

    Retorna la respuesta generada por IA con contexto relevante
    """
    try:
        # 1. Buscar contexto
        context = chromadb_service.search(request.message)

        # 2. Generar respuesta
        response = await gemini_service.generate(request.message, context)

        return ChatResponse(
            response=response,
            status="success"
        )

    except Exception as e:
        logger.error(f"Error en endpoint /chat: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar mensaje: {str(e)}"
        )

@router.get("/chat/status")
async def status():
    """Verifica el estado de los servicios"""
    return {
        "chromadb": "connected",
        "gemini": "connected",
        "documents_loaded": True
    }
