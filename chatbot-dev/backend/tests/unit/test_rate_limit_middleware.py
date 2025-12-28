import pytest
from fastapi import Request

# Esqueleto de tests para rate limit middleware

@pytest.mark.skip(reason="Mockear request y rate limiter")
def test_require_rate_limit_allows_when_under_limit():
    # TODO: construir Request mock y simular rate_limiter.allow
    assert True

@pytest.mark.skip(reason="Mockear request y rate limiter")
def test_require_rate_limit_blocks_when_exceeded():
    # TODO: simular response 429
    assert True
