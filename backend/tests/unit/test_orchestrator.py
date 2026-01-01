"""
Tests unitarios para el orquestador híbrido
"""

import pytest
from unittest.mock import MagicMock, patch
from app.core.orchestrator import HybridRAGOrchestrator

@pytest.mark.unit
class TestHybridOrchestrator:
    """Tests para el HybridRAGOrchestrator"""
    
    def test_orchestrator_initialization(self):
        """Test inicialización del orquestador"""
        with patch('app.core.factory.ProviderFactory.create_all_providers') as mock_factory:
            mock_factory.return_value = {
                'llm': MagicMock(),
                'embedding': MagicMock(),
                'vector_store': MagicMock(),
                'document_processor': MagicMock(),
                'cache': MagicMock()
            }
            
            orchestrator = HybridRAGOrchestrator()
            
            assert orchestrator is not None
            assert orchestrator.llm_provider is not None
            assert orchestrator.embedding_provider is not None
            assert orchestrator.vector_store is not None
    
    def test_process_hybrid_request_basic(self, mock_orchestrator):
        """Test procesamiento básico de request"""
        result = mock_orchestrator.process_hybrid_request(
            message="Test message",
            client_identifier="test_client",
            user_context=None,
            target_language="es"
        )
        
        assert result['success'] == True
        assert 'response' in result
        assert 'metadata' in result
    
    @patch('app.utils.rate_limiter.check_rate_limit')
    def test_rate_limiting_check(self, mock_rate_limit):
        """Test verificación de rate limiting"""
        mock_rate_limit.return_value = {
            'allowed': False,
            'retry_after': 60
        }
        
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            orchestrator = HybridRAGOrchestrator()
            result = orchestrator.process_hybrid_request(
                message="Test",
                client_identifier="test_client"
            )
            
            assert result['success'] == False
            assert 'rate_limit_exceeded' in result['metadata']['flow_path']
    
    @patch('app.utils.sanitizer.process_user_input')
    def test_input_validation(self, mock_sanitizer):
        """Test validación de entrada"""
        mock_sanitizer.return_value = {
            'is_valid': False,
            'warnings': ['Input too long']
        }
        
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            with patch('app.utils.rate_limiter.check_rate_limit') as mock_rate:
                mock_rate.return_value = {'allowed': True}
                
                orchestrator = HybridRAGOrchestrator()
                result = orchestrator.process_hybrid_request(
                    message="Test",
                    client_identifier="test_client"
                )
                
                assert result['success'] == False
                assert 'input_validation_failed' in result['metadata']['flow_path']
    
    def test_cache_hit_flow(self):
        """Test flujo cuando hay cache hit"""
        with patch('app.core.factory.ProviderFactory.create_all_providers') as mock_factory:
            mock_cache = MagicMock()
            mock_cache.get.return_value = {
                'success': True,
                'response': 'Cached response',
                'from_cache': True
            }
            
            mock_factory.return_value = {
                'llm': MagicMock(),
                'embedding': MagicMock(),
                'vector_store': MagicMock(),
                'document_processor': MagicMock(),
                'cache': mock_cache
            }
            
            with patch('app.utils.rate_limiter.check_rate_limit') as mock_rate:
                mock_rate.return_value = {'allowed': True}
                
                with patch('app.utils.sanitizer.process_user_input') as mock_input:
                    mock_input.return_value = {
                        'is_valid': True,
                        'processed_message': 'Test'
                    }
                    
                    with patch('app.services.safety_checker.check_input_safety') as mock_safety:
                        mock_safety.return_value = {'is_safe': True}
                        
                        orchestrator = HybridRAGOrchestrator()
                        result = orchestrator.process_hybrid_request(
                            message="Test",
                            client_identifier="test_client"
                        )
                        
                        assert result['from_cache'] == True
                        assert 'cache_hit' in result['metadata']['flow_path']
    
    def test_faq_classification_flow(self):
        """Test flujo de clasificación FAQ"""
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            with patch('app.utils.faq_checker.classify_user_message') as mock_faq:
                mock_faq.return_value = {
                    'is_faq': True,
                    'confidence': 0.95,
                    'response': 'FAQ response',
                    'category': 'experience'
                }
                
                # Patch todo el pipeline hasta FAQ
                with patch('app.utils.rate_limiter.check_rate_limit') as mock_rate:
                    mock_rate.return_value = {'allowed': True}
                    
                    with patch('app.utils.sanitizer.process_user_input') as mock_input:
                        mock_input.return_value = {
                            'is_valid': True,
                            'processed_message': 'Test'
                        }
                        
                        with patch('app.services.safety_checker.check_input_safety') as mock_safety:
                            mock_safety.return_value = {'is_safe': True}
                            
                            with patch('app.utils.section_templates.validate_message_section') as mock_section:
                                mock_section.return_value = {'is_valid': True}
                                
                                orchestrator = HybridRAGOrchestrator()
                                orchestrator.cache_provider = None  # No cache
                                orchestrator._check_services_health = MagicMock(return_value={
                                    'llm_available': True,
                                    'vector_store_available': True,
                                    'embedding_available': True
                                })
                                
                                result = orchestrator.process_hybrid_request(
                                    message="¿Cuál es tu experiencia?",
                                    client_identifier="test_client"
                                )
                                
                                assert 'faq_response' in result.get('metadata', {}).get('flow_path', [])
    
    def test_emergency_mode_activation(self):
        """Test activación del modo de emergencia"""
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            with patch('app.services.emergency_mode.check_emergency_activation') as mock_check:
                mock_check.return_value = False  # No services available
                
                with patch('app.services.emergency_mode.emergency_mode') as mock_emergency:
                    mock_emergency.is_active = True
                    
                    with patch('app.services.emergency_mode.handle_emergency') as mock_handle:
                        mock_handle.return_value = {
                            'success': True,
                            'response': 'Emergency response'
                        }
                        
                        # Patch pipeline inicial
                        with patch('app.utils.rate_limiter.check_rate_limit') as mock_rate:
                            mock_rate.return_value = {'allowed': True}
                            
                            orchestrator = HybridRAGOrchestrator()
                            orchestrator._check_services_health = MagicMock(return_value={
                                'llm_available': False,
                                'vector_store_available': False,
                                'embedding_available': False
                            })
                            
                            result = orchestrator.process_hybrid_request(
                                message="Test",
                                client_identifier="test_client"
                            )
                            
                            assert 'emergency_mode' in result.get('metadata', {}).get('flow_path', [])
    
    def test_safety_check_blocks_unsafe_content(self):
        """Test que el safety check bloquea contenido no seguro"""
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            with patch('app.services.safety_checker.check_input_safety') as mock_safety:
                mock_safety.return_value = {
                    'is_safe': False,
                    'issues': ['inappropriate_content']
                }
                
                with patch('app.utils.rate_limiter.check_rate_limit') as mock_rate:
                    mock_rate.return_value = {'allowed': True}
                    
                    with patch('app.utils.sanitizer.process_user_input') as mock_input:
                        mock_input.return_value = {
                            'is_valid': True,
                            'processed_message': 'Unsafe content'
                        }
                        
                        orchestrator = HybridRAGOrchestrator()
                        result = orchestrator.process_hybrid_request(
                            message="Unsafe content",
                            client_identifier="test_client"
                        )
                        
                        assert result['success'] == False
                        assert 'input_unsafe' in result['metadata']['flow_path']
    
    def test_i18n_translation_applied(self):
        """Test que la traducción i18n se aplica correctamente"""
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            with patch('app.services.i18n_service.translate_response') as mock_i18n:
                mock_i18n.return_value = {
                    'success': True,
                    'response': 'Translated response',
                    'i18n_applied': True,
                    'language': 'en'
                }
                
                # Setup full pipeline mocks
                with patch('app.utils.rate_limiter.check_rate_limit') as mock_rate:
                    mock_rate.return_value = {'allowed': True}
                    
                    orchestrator = HybridRAGOrchestrator()
                    orchestrator._generate_rag_response = MagicMock(return_value={
                        'success': True,
                        'response': 'Original response'
                    })
                    
                    result = orchestrator.process_hybrid_request(
                        message="Test",
                        client_identifier="test_client",
                        target_language="en"
                    )
                    
                    mock_i18n.assert_called()
    
    def test_system_status_reporting(self):
        """Test reporte de estado del sistema"""
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            orchestrator = HybridRAGOrchestrator()
            status = orchestrator.get_system_status()
            
            assert 'initialized' in status
            assert 'providers' in status
            assert 'hybrid_components' in status
    
    def test_document_reload(self):
        """Test recarga de documentos"""
        with patch('app.core.factory.ProviderFactory.create_all_providers'):
            orchestrator = HybridRAGOrchestrator()
            
            with patch.object(orchestrator, '_initialize_documents') as mock_init:
                result = orchestrator.reload_documents()
                
                mock_init.assert_called()
                assert 'success' in result
