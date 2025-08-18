import pytest

# Fixtures globales para tests (esqueleto)

@pytest.fixture
def sample_message():
    return "¿Qué experiencia tienes?"

@pytest.fixture
def dummy_client_identifier():
    return "test_client"

# TODO: añadir fixtures para orchestrator con proveedores mock, temp dirs, TestClient, etc.
