"""
Unit tests for Rate Limiter component
"""

import pytest
from unittest.mock import Mock, patch
import time

class TestRateLimiter:
    """Test suite for rate limiter functionality"""
    
    def test_rate_limit_allows_under_limit(self):
        """Test that requests under limit are allowed"""
        from app.utils.rate_limiter import check_rate_limit
        
        result = check_rate_limit("test_client", "test", limit=5, window=60)
        assert result['allowed'] == True
        assert result['remaining'] >= 4
    
    def test_rate_limit_blocks_over_limit(self):
        """Test that requests over limit are blocked"""
        from app.utils.rate_limiter import check_rate_limit
        
        # Exhaust limit
        for i in range(5):
            check_rate_limit("test_client_2", "test", limit=5, window=60)
        
        # Next request should be blocked
        result = check_rate_limit("test_client_2", "test", limit=5, window=60)
        assert result['allowed'] == False
        assert result['retry_after'] > 0
    
    def test_rate_limit_resets_after_window(self):
        """Test that rate limit resets after time window"""
        from app.utils.rate_limiter import check_rate_limit
        
        # Use very short window for testing
        check_rate_limit("test_client_3", "test", limit=1, window=1)
        
        # Should be blocked immediately
        result = check_rate_limit("test_client_3", "test", limit=1, window=1)
        assert result['allowed'] == False
        
        # Wait for window to expire
        time.sleep(1.1)
        
        # Should be allowed again
        result = check_rate_limit("test_client_3", "test", limit=1, window=1)
        assert result['allowed'] == True
    
    def test_different_categories_independent(self):
        """Test that different categories have independent limits"""
        from app.utils.rate_limiter import check_rate_limit
        
        # Use limit for category 1
        for i in range(3):
            result = check_rate_limit("test_client_4", "cat1", limit=3, window=60)
            assert result['allowed'] == True
        
        # Category 1 should be blocked
        result = check_rate_limit("test_client_4", "cat1", limit=3, window=60)
        assert result['allowed'] == False
        
        # Category 2 should still be allowed
        result = check_rate_limit("test_client_4", "cat2", limit=3, window=60)
        assert result['allowed'] == True
    
    def test_get_client_identifier(self):
        """Test client identifier extraction"""
        from app.utils.rate_limiter import get_client_identifier
        
        # Mock request object
        mock_request = Mock()
        mock_request.remote_addr = "192.168.1.1"
        mock_request.headers = {}
        
        identifier = get_client_identifier(mock_request)
        assert identifier == "ip:192.168.1.1"
        
        # Test with API key
        mock_request.headers = {"X-API-Key": "test-key"}
        identifier = get_client_identifier(mock_request)
        assert identifier == "api_key:test-key"
    
    def test_rate_limiter_stats(self):
        """Test rate limiter statistics"""
        from app.utils.rate_limiter import rate_limiter
        
        # Clear stats
        rate_limiter.reset_stats()
        
        # Generate some activity
        rate_limiter.check_rate_limit("test_stats", "test", 10, 60)
        rate_limiter.check_rate_limit("test_stats", "test", 10, 60)
        
        stats = rate_limiter.get_global_stats()
        assert stats['total_requests'] >= 2
        assert 'clients' in stats
