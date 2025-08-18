import pytest

# Tests unitarios para el orquestador híbrido (esqueleto)

@pytest.mark.skip(reason="Implementar mocks de proveedores y fixtures")
def test_process_hybrid_request_basic_flow():
    """Verifica que process_hybrid_request devuelve estructura esperada en flow happy-path"""
    # TODO: crear fixture `orchestrator` con proveedores mock
    # orchestrator = ...
    # result = orchestrator.process_hybrid_request("¿Qué experiencia tienes?", "test_client")
    # assert result["success"] is True
    assert True


@pytest.mark.skip(reason="Implementar mocks de proveedores y fixtures")
def test_cache_hit_returns_cached_response():
    """Verifica que si cache tiene respuesta, se retorna sin llamar al LLM"""
    # TODO: stub cache con key prepopulada
    assert True
