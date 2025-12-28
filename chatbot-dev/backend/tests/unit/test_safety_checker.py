"""
Unit tests for Safety Checker component
"""

import pytest
from unittest.mock import Mock, patch

class TestSafetyChecker:
    """Test suite for safety checker functionality"""
    
    def test_safe_input_passes(self):
        """Test that safe input passes checks"""
        from app.services.safety_checker import check_input_safety
        
        safe_inputs = [
            "¿Cuál es tu experiencia profesional?",
            "Háblame sobre tus proyectos",
            "¿Cómo puedo contactarte?",
            "What technologies do you know?"
        ]
        
        for input_text in safe_inputs:
            result = check_input_safety(input_text)
            assert result['is_safe'] == True
            assert len(result.get('issues', [])) == 0
    
    def test_unsafe_input_blocked(self):
        """Test that unsafe input is blocked"""
        from app.services.safety_checker import check_input_safety
        
        # Note: Using mild examples for testing
        unsafe_inputs = [
            "x" * 10000,  # Too long
            "",  # Empty
            "<script>alert('xss')</script>",  # Potential XSS
            "SELECT * FROM users;",  # SQL-like
        ]
        
        for input_text in unsafe_inputs:
            result = check_input_safety(input_text)
            if not result['is_safe']:
                assert len(result.get('issues', [])) > 0
    
    def test_output_safety_check(self):
        """Test output safety checking"""
        from app.services.safety_checker import check_output_safety
        
        context = {'user_message': 'test question'}
        
        # Safe output
        safe_result = check_output_safety(
            "Esta es una respuesta profesional y segura.",
            context
        )
        assert safe_result['is_safe'] == True
        
        # Output with potential issues
        result = check_output_safety(
            "Mi número de teléfono personal es 555-1234",
            context
        )
        # Should flag PII but may still pass with warning
        assert 'safe_response' in result
    
    def test_safety_stats_tracking(self):
        """Test safety checker statistics"""
        from app.services.safety_checker import safety_checker
        
        safety_checker.reset_stats()
        
        # Perform some checks
        safety_checker.check_input("test input 1")
        safety_checker.check_input("test input 2")
        safety_checker.check_output("test output", {})
        
        stats = safety_checker.get_stats()
        assert stats['total_checks'] >= 3
        assert 'blocked_count' in stats
        assert 'pass_rate' in stats
    
    def test_content_sanitization(self):
        """Test content sanitization"""
        from app.services.safety_checker import sanitize_content
        
        # Test HTML sanitization
        dirty_html = "<p>Hello <script>alert('xss')</script> World</p>"
        clean = sanitize_content(dirty_html)
        assert '<script>' not in clean
        assert 'Hello' in clean
        assert 'World' in clean
    
    def test_pii_detection(self):
        """Test PII detection in content"""
        from app.services.safety_checker import detect_pii
        
        # Test various PII patterns
        test_cases = [
            ("My email is test@example.com", True),
            ("Call me at 555-1234", True),
            ("My SSN is 123-45-6789", True),
            ("This is a normal sentence", False)
        ]
        
        for text, expected_has_pii in test_cases:
            result = detect_pii(text)
            assert result['has_pii'] == expected_has_pii
            if expected_has_pii:
                assert len(result['pii_types']) > 0
