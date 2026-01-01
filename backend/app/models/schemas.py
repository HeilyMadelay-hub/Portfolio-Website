from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Mensaje del usuario")
    context: Optional[str] = None
    language: Optional[str] = "es"
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Qué experiencia tienes en Python?"
            }
        }

class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    metadata: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: str
    status: str = "error"
