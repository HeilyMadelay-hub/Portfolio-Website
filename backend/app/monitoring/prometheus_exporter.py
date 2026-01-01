"""
Prometheus exporter helper para exponer métricas reales desde la app
- registra métricas básicas: requests, response_time, cache_hits, errors
- funciona con prometheus_client
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from typing import Optional

registry = CollectorRegistry()

REQUEST_COUNTER = Counter('portfolio_requests_total', 'Total requests', ['endpoint', 'method'], registry=registry)
RESPONSE_TIME = Histogram('portfolio_response_duration_seconds', 'Response time seconds', ['endpoint'], registry=registry)
CACHE_HITS = Counter('portfolio_cache_hits_total', 'Cache hits', ['endpoint'], registry=registry)
ERROR_COUNTER = Counter('portfolio_errors_total', 'Total errors', ['endpoint', 'type'], registry=registry)


def get_metrics():
    return generate_latest(registry), CONTENT_TYPE_LATEST


def inc_request(endpoint: str, method: str = 'GET'):
    REQUEST_COUNTER.labels(endpoint=endpoint, method=method).inc()


def observe_response_time(endpoint: str, seconds: float):
    RESPONSE_TIME.labels(endpoint=endpoint).observe(seconds)


def inc_cache_hit(endpoint: str):
    CACHE_HITS.labels(endpoint=endpoint).inc()


def inc_error(endpoint: str, err_type: str = 'internal'):
    ERROR_COUNTER.labels(endpoint=endpoint, type=err_type).inc()
