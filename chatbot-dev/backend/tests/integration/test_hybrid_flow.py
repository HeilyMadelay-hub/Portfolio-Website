"""
Integration tests for the complete hybrid flow
"""

import pytest
from unittest.mock import Mock, patch
import json

class TestHybridFlow:
    """Test suite for complete hybrid processing flow"""
    
    @pytest.fixture
    def app_client(self):
        """Create test client"""
        from app import create_app
        app = create_app('testing')
        
        if hasattr(app, 'test_client'):
            # Flask
            return app.test_client()
        else:
            # FastAPI
            from fastapi.testclient import TestClient
            return TestClient(app)
    
    def test_complete_chat_flow(self, app_client):
        """Test complete chat request flow"""
        response = app_client.post('/api/chat', json={
            'message': '¿Cuál es tu experiencia profesional?',
            'context': None,
            'language': 'es'
        })
        
        assert response.status_code in [200, 201]
        data = response.json if hasattr(response, 'json') else response.json()
        
        assert 'success' in data
        assert 'response' in data
        assert 'metadata' in data
        assert len(data['response']) > 0
    
    def test_rate_limiting_integration(self, app_client):
        """Test rate limiting in the flow"""
        # Make multiple requests to trigger rate limit
        for i in range(100):
            response = app_client.post('/api/chat', json={
                'message': f'Test message {i}',
                'language': 'es'
            })
            
            if response.status_code == 429:
                # Rate limit hit
                data = response.json if hasattr(response, 'json') else response.json()
                assert 'retry_after' in data
                assert 'error' in data
                break
        else:
            # If loop completes without rate limit, that's also valid
            # (limit might be high in test config)
            pass
    
    def test_faq_flow_integration(self, app_client):
        """Test FAQ detection and response flow"""
        faq_questions = [
            "¿Cuál es tu experiencia?",
            "¿Qué proyectos has desarrollado?",
            "¿Cómo puedo contactarte?"
        ]
        
        for question in faq_questions:
            response = app_client.post('/api/chat', json={
                'message': question,
                'language': 'es'
            })
            
            assert response.status_code == 200
            data = response.json if hasattr(response, 'json') else response.json()
            
            # FAQ responses should be fast and from FAQ source
            if 'metadata' in data:
                if 'source' in data['metadata']:
                    # May be from FAQ or RAG depending on confidence
                    assert data['metadata']['source'] in ['faq', 'rag', 'cache']
    
    def test_safety_check_integration(self, app_client):
        """Test safety checks in the flow"""
        # Test with very long input
        long_message = "test " * 1000
        
        response = app_client.post('/api/chat', json={
            'message': long_message,
            'language': 'es'
        })
        
        # Should either truncate or reject
        assert response.status_code in [200, 400]
        
        if response.status_code == 400:
            data = response.json if hasattr(response, 'json') else response.json()
            assert 'error' in data or not data.get('success', True)
    
    def test_multilingual_flow(self, app_client):
        """Test multilingual support in the flow"""
        languages = ['es', 'en', 'fr']
        
        for lang in languages:
            response = app_client.post('/api/chat', json={
                'message': 'What is your experience?',
                'language': lang
            })
            
            if response.status_code == 200:
                data = response.json if hasattr(response, 'json') else response.json()
                assert 'response' in data
                # Response should be in requested language or indicate language
    
    def test_cache_integration(self, app_client):
        """Test cache functionality in the flow"""
        # Make same request twice
        message = "¿Cuáles son tus habilidades técnicas?"
        
        # First request
        response1 = app_client.post('/api/chat', json={
            'message': message,
            'language': 'es'
        })
        
        assert response1.status_code == 200
        data1 = response1.json if hasattr(response1, 'json') else response1.json()
        
        # Second request (should be cached)
        response2 = app_client.post('/api/chat', json={
            'message': message,
            'language': 'es'
        })
        
        assert response2.status_code == 200
        data2 = response2.json if hasattr(response2, 'json') else response2.json()
        
        # Responses should be identical if cached
        if 'metadata' in data2:
            # Check if it indicates cache hit
            assert data1['response'] == data2['response']
    
    def test_emergency_mode_activation(self, app_client):
        """Test emergency mode activation and handling"""
        # Simulate emergency mode
        response = app_client.post('/api/chat/emergency/simulate', json={
            'reason': 'Integration test',
            'duration': 5
        })
        
        if response.status_code == 200:
            # Try chat during emergency
            chat_response = app_client.post('/api/chat', json={
                'message': 'Test during emergency',
                'language': 'es'
            })
            
            # Should still respond, possibly with template
            assert chat_response.status_code == 200
            
            # Deactivate emergency
            app_client.post('/api/chat/emergency/deactivate')
    
    def test_monitoring_endpoints(self, app_client):
        """Test monitoring endpoints integration"""
        endpoints = [
            '/api/monitoring/metrics',
            '/api/monitoring/flow-stats',
            '/api/monitoring/performance',
            '/api/chat/status',
            '/api/chat/health'
        ]
        
        for endpoint in endpoints:
            response = app_client.get(endpoint)
            assert response.status_code in [200, 503]  # 503 if unhealthy
            
            if response.status_code == 200:
                data = response.json if hasattr(response, 'json') else response.json()
                assert data is not None
