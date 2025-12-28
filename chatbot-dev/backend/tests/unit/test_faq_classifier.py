"""
Unit tests for FAQ Classifier component
"""

import pytest
from unittest.mock import Mock, patch

class TestFAQClassifier:
    """Test suite for FAQ classifier functionality"""
    
    def test_classify_faq_question(self):
        """Test classification of FAQ questions"""
        from app.utils.faq_checker import classify_user_message
        
        # Test common FAQ questions
        test_cases = [
            ("¿Cuál es tu experiencia?", True, "experience"),
            ("¿Qué proyectos has hecho?", True, "projects"),
            ("¿Cómo puedo contactarte?", True, "contact"),
            ("Háblame sobre ti", True, "about"),
            ("Una pregunta muy específica y rara", False, None)
        ]
        
        for question, expected_is_faq, expected_category in test_cases:
            result = classify_user_message(question)
            
            if expected_is_faq:
                assert result['is_faq'] == True
                assert result['confidence'] > 0.5
                if expected_category:
                    assert result['category'] == expected_category
            else:
                assert result['is_faq'] == False or result['confidence'] < 0.5
    
    def test_faq_response_generation(self):
        """Test FAQ response generation"""
        from app.utils.faq_checker import classify_user_message
        
        result = classify_user_message("¿Cuál es tu experiencia profesional?")
        
        assert 'response' in result
        assert len(result['response']) > 0
        assert result['is_faq'] == True
    
    def test_faq_confidence_scores(self):
        """Test confidence score calculation"""
        from app.utils.faq_checker import classify_user_message
        
        # Exact match should have high confidence
        result = classify_user_message("¿Cuál es tu experiencia?")
        assert result['confidence'] > 0.8
        
        # Partial match should have lower confidence
        result = classify_user_message("experiencia")
        assert result['confidence'] > 0.3
        assert result['confidence'] < 0.8
        
        # No match should have very low confidence
        result = classify_user_message("askdjfhaskjdhfkajsdhf")
        assert result['confidence'] < 0.3
    
    def test_faq_classifier_stats(self):
        """Test FAQ classifier statistics tracking"""
        from app.utils.faq_checker import faq_classifier
        
        # Reset stats
        faq_classifier.reset_stats()
        
        # Generate some classifications
        faq_classifier.classify("test question 1")
        faq_classifier.classify("test question 2")
        
        stats = faq_classifier.get_stats()
        assert stats['total_classifications'] >= 2
        assert 'faq_hit_rate' in stats
        assert 'categories' in stats
    
    def test_multilingual_faq_classification(self):
        """Test FAQ classification in multiple languages"""
        from app.utils.faq_checker import classify_user_message
        
        # Test English questions
        result_en = classify_user_message("What is your experience?")
        assert result_en['is_faq'] == True
        
        # Test Spanish questions (default)
        result_es = classify_user_message("¿Cuál es tu experiencia?")
        assert result_es['is_faq'] == True
        
        # Both should map to same category
        assert result_en.get('category') == result_es.get('category')
