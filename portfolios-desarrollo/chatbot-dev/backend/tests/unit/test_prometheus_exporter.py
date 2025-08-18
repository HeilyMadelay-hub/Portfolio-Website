import pytest

# Tests unitarios para el exporter Prometheus

def test_metrics_registry_importable():
    try:
        from app.monitoring.prometheus_exporter import get_metrics, inc_request, observe_response_time, inc_cache_hit, inc_error
    except Exception as e:
        pytest.skip(f"prometheus_client no instalado en entorno de test: {e}")

    # Llamar a get_metrics y validar que retorne bytes y content-type
    content, content_type = get_metrics()
    assert isinstance(content, (bytes, bytearray))
    assert isinstance(content_type, str)

    # Probar incrementos básicos (no fallar)
    inc_request(endpoint='/test', method='GET')
    observe_response_time(endpoint='/test', seconds=0.123)
    inc_cache_hit(endpoint='cache_test')
    inc_error(endpoint='/test', err_type='unit_test')
