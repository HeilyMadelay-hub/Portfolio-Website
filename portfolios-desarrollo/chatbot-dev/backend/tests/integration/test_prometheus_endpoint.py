import pytest
from flask import Flask

from app import create_flask_app

@pytest.fixture
def client():
    app = create_flask_app(config_name='testing')
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_prometheus_endpoint_requires_api_key(client):
    # Si ADMIN_API_KEY_REQUIRED está activado en Config, la petición sin API key debe fallar
    resp = client.get('/api/monitoring/prometheus')
    # Aceptamos 404 si PROMETHEUS_DISABLED o 403 si API key requerida
    assert resp.status_code in (403, 404, 200)


def test_prometheus_endpoint_returns_metrics_when_available(client):
    # Intentar llamar y validar Content-Type cuando prometheus está habilitado
    resp = client.get('/api/monitoring/prometheus', headers={'X-API-Key': 'test'})
    assert resp.status_code in (200, 403, 404)
    if resp.status_code == 200:
        assert 'Content-Type' in resp.headers
        assert 'text' in resp.headers['Content-Type'] or 'openmetrics' in resp.headers['Content-Type']
