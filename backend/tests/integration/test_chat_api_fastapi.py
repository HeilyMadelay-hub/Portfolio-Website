import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routes import chat as chat_routes


class DummyChromaService:
    """Servicio ChromaDB simulado para tests FastAPI"""

    def search(self, message: str):  # pragma: no cover - lógica trivial de stub
        return [
            {
                "content": "Contenido simulado para pruebas",
                "score": 0.99,
            }
        ]


class DummyGeminiService:
    """Servicio Gemini simulado para tests FastAPI"""

    async def generate(self, message: str, context):  # pragma: no cover
        return f"Respuesta de prueba para: {message}"


def create_test_app() -> FastAPI:
    """Construye una app FastAPI mínima con el router de chat y servicios stub."""
    app = FastAPI()

    # Sustituir servicios reales por dummies para no depender de infra externa
    chat_routes.chromadb_service = DummyChromaService()
    chat_routes.gemini_service = DummyGeminiService()

    app.include_router(chat_routes.router, prefix="/api")
    return app


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    app = create_test_app()
    return TestClient(app)


def test_chat_endpoint_returns_success_response(test_client: TestClient):
    payload = {"message": "Hola", "language": "es"}

    response = test_client.post("/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "response" in data
    assert isinstance(data["response"], str)
    assert "Hola" in data["response"]


def test_status_endpoint_returns_expected_structure(test_client: TestClient):
    response = test_client.get("/api/chat/status")

    assert response.status_code == 200
    data = response.json()
    # Estructura básica según implementación actual
    assert "chromadb" in data
    assert "gemini" in data
    assert "documents_loaded" in data
