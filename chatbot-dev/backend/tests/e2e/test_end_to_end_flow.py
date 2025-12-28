import pytest

# Esqueleto para pruebas e2e (puede ser ejecutado en CI con servicios levantados)

@pytest.mark.skip(reason="Requiere entorno docker-compose con servicios up (backend, chromadb)")
def test_end_to_end_chat_flow():
    # TODO: ejecutar petición real a backend y validar respuesta completa
    assert True
