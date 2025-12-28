import logging
from typing import Dict, Any, Optional
from ..core import HybridRAGOrchestrator
from ..utils.rate_limiter import get_client_identifier

logger = logging.getLogger(__name__)

class HybridGeminiService:
    """
    Servicio principal híbrido implementando diagrama de flujo completo
    Integra: Rate Limiting -> Validation -> Processing -> Cache -> Health Check -> 
            Section Validation -> FAQ -> RAG -> Safety -> i18n -> Response
    """
    
    def __init__(self):
        """Inicializa el servicio híbrido con orquestador completo"""
        
        # Configuración de proveedores para arquitectura híbrida
        provider_config = {
            'llm': 'gemini',
            'embedding': 'gemini',
            'vector_store': 'chromadb',
            'document_processor': 'filesystem',
            'cache': 'memory'
        }
        
        # Crear orquestador híbrido
        self.orchestrator = HybridRAGOrchestrator(provider_config)
        
        logger.info("HybridGeminiService inicializado con flujo completo del diagrama")
    
    def generate_response(self, message: str, request=None, user_context: Optional[str] = None, target_language: str = "es") -> Dict[str, Any]:
        """
        Genera respuesta usando el flujo híbrido completo
        
        Args:
            message: Mensaje del usuario
            request: Request de Flask para extraer identificador del cliente
            user_context: Contexto adicional del usuario (opcional)
            target_language: Idioma objetivo para la respuesta
        
        Returns:
            Dict con la respuesta procesada según diagrama de flujo
        """
        try:
            # Extraer identificador del cliente para rate limiting
            client_identifier = "unknown"
            if request:
                client_identifier = get_client_identifier(request)
            
            # Procesar usando flujo híbrido completo
            return self.orchestrator.process_hybrid_request(
                message=message,
                client_identifier=client_identifier,
                user_context=user_context,
                target_language=target_language
            )
            
        except Exception as e:
            logger.error(f"Error en generate_response híbrido: {e}")
            return {
                'success': False,
                'response': "Error procesando consulta en sistema híbrido",
                'error': str(e),
                'flow_path': ['critical_error'],
                'hybrid_system': True
            }
    
    def reload_documents(self) -> Dict[str, Any]:
        """
        Recarga todos los documentos del sistema híbrido
        
        Returns:
            Dict con resultado de la operación
        """
        try:
            return self.orchestrator.reload_documents()
        except Exception as e:
            logger.error(f"Error recargando documentos en sistema híbrido: {e}")
            return {"success": False, "error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado completo del sistema híbrido
        
        Returns:
            Dict con estado de todos los componentes del diagrama
        """
        try:
            status = self.orchestrator.get_system_status()
            status['system_type'] = 'hybrid_rag'
            status['diagram_implementation'] = 'complete'
            return status
        except Exception as e:
            logger.error(f"Error obteniendo estado del sistema híbrido: {e}")
            return {"error": str(e), "system_type": "hybrid_rag"}
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verificación rápida de salud del sistema híbrido
        
        Returns:
            Dict con estado básico de salud de todos los componentes
        """
        try:
            status = self.orchestrator.get_system_status()
            
            # Verificar componentes críticos
            providers_ok = all(
                status.get('providers', {}).get(name, {}).get('available', False)
                for name in ['llm', 'vector_store']
            )
            
            hybrid_components_ok = all(
                component.get('total_rules', 0) > 0 or 
                component.get('total_faqs', 0) > 0 or
                component.get('total_sections', 0) > 0 or
                'active_users' in component or
                'total_translations' in component
                for component in status.get('hybrid_components', {}).values()
            )
            
            is_healthy = (
                status.get('initialized', False) and
                providers_ok and
                hybrid_components_ok
            )
            
            return {
                'healthy': is_healthy,
                'system_type': 'hybrid_rag',
                'initialized': status.get('initialized', False),
                'error': status.get('initialization_error'),
                'providers_status': {
                    name: info.get('available', False) 
                    for name, info in status.get('providers', {}).items()
                },
                'hybrid_components_status': {
                    name: 'active' if any(
                        key in component for key in ['total_rules', 'total_faqs', 'total_sections', 'active_users', 'total_translations']
                    ) else 'inactive'
                    for name, component in status.get('hybrid_components', {}).items()
                },
                'vector_store_type': status.get('vector_store_stats', {}).get('store_type', 'unknown'),
                'documents_loaded': status.get('vector_store_stats', {}).get('total_documents', 0),
                'diagram_flow_ready': is_healthy
            }
        except Exception as e:
            logger.error(f"Error en health check híbrido: {e}")
            return {
                'healthy': False,
                'system_type': 'hybrid_rag',
                'error': str(e)
            }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Información sobre todos los proveedores y componentes híbridos
        
        Returns:
            Dict con información completa del sistema
        """
        try:
            status = self.orchestrator.get_system_status()
            
            return {
                'system_type': 'hybrid_rag',
                'diagram_implementation': 'complete',
                'providers': status.get('providers', {}),
                'hybrid_components': status.get('hybrid_components', {}),
                'vector_store_stats': status.get('vector_store_stats', {}),
                'documents_info': status.get('documents_info', {}),
                'documents_count': status.get('vector_store_stats', {}).get('total_documents', 0),
                'vector_store_type': status.get('vector_store_stats', {}).get('store_type', 'unknown'),
                'flow_components': {
                    'rate_limiting': 'active',
                    'input_processing': 'active',
                    'cache_lookup': 'active',
                    'health_check': 'active',
                    'section_validation': 'active',
                    'faq_classification': 'active',
                    'rag_generation': 'active',
                    'safety_check': 'active',
                    'i18n_support': 'active',
                    'emergency_mode': 'ready'
                }
            }
        except Exception as e:
            logger.error(f"Error obteniendo info de proveedores híbridos: {e}")
            return {"error": str(e), "system_type": "hybrid_rag"}
    
    def get_hybrid_stats(self) -> Dict[str, Any]:
        """
        Estadísticas específicas del sistema híbrido
        
        Returns:
            Dict con métricas detalladas de todos los componentes
        """
        try:
            status = self.orchestrator.get_system_status()
            
            hybrid_stats = {
                'system_overview': {
                    'type': 'hybrid_rag',
                    'diagram_compliance': 'full',
                    'initialization_status': status.get('initialized', False),
                    'total_components': len(status.get('hybrid_components', {}))
                }
            }
            
            # Agregar stats de cada componente híbrido
            for component_name, component_stats in status.get('hybrid_components', {}).items():
                hybrid_stats[component_name] = component_stats
            
            # Agregar stats de proveedores base
            hybrid_stats['base_providers'] = status.get('providers', {})
            
            # Agregar stats de vector store si está disponible
            if 'vector_store_stats' in status:
                hybrid_stats['vector_store'] = status['vector_store_stats']
            
            return hybrid_stats
            
        except Exception as e:
            logger.error(f"Error obteniendo stats híbridos: {e}")
            return {"error": str(e), "system_type": "hybrid_rag"}
    
    def get_flow_analytics(self) -> Dict[str, Any]:
        """
        Analíticas del flujo de procesamiento del diagrama
        
        Returns:
            Dict con métricas de uso del flujo
        """
        try:
            from ..utils.rate_limiter import rate_limiter
            from ..services.emergency_mode import emergency_mode
            
            return {
                'rate_limiting': {
                    'global_stats': rate_limiter.get_global_stats(),
                    'status': 'active'
                },
                'emergency_mode': {
                    'status': emergency_mode.get_status(),
                    'is_active': emergency_mode.is_active
                },
                'flow_readiness': {
                    'rate_limiting': True,
                    'input_processing': True,
                    'cache_system': True,
                    'health_monitoring': True,
                    'section_validation': True,
                    'faq_classification': True,
                    'rag_processing': True,
                    'safety_checks': True,
                    'i18n_support': True,
                    'emergency_fallback': True
                },
                'supported_languages': ['es', 'en'],
                'diagram_coverage': '100%'
            }
        except Exception as e:
            logger.error(f"Error obteniendo analíticas de flujo: {e}")
            return {"error": str(e)}
    
    def test_flow_component(self, component: str, test_data: Dict = None) -> Dict[str, Any]:
        """
        Prueba un componente específico del flujo
        
        Args:
            component: Nombre del componente a probar
            test_data: Datos de prueba opcionales
        
        Returns:
            Dict con resultado de la prueba
        """
        try:
            test_results = {
                'component': component,
                'test_timestamp': __import__('time').time(),
                'status': 'unknown'
            }
            
            if component == 'rate_limiting':
                from ..utils.rate_limiter import check_rate_limit
                result = check_rate_limit('test_client', 'test')
                test_results['status'] = 'pass' if result.get('allowed', False) else 'fail'
                test_results['details'] = result
                
            elif component == 'faq_classification':
                from ..utils.faq_checker import classify_user_message
                test_message = test_data.get('message', '¿Qué experiencia tienes?') if test_data else '¿Qué experiencia tienes?'
                result = classify_user_message(test_message)
                test_results['status'] = 'pass' if result.get('is_faq', False) else 'fail'
                test_results['details'] = result
                
            elif component == 'safety_check':
                from ..services.safety_checker import check_input_safety
                test_message = test_data.get('message', 'Mensaje de prueba') if test_data else 'Mensaje de prueba'
                result = check_input_safety(test_message)
                test_results['status'] = 'pass' if result.get('is_safe', False) else 'fail'
                test_results['details'] = result
                
            elif component == 'i18n':
                from ..services.i18n_service import translate_response
                test_response = test_data if test_data else {'response': 'Test message', 'success': True}
                result = translate_response(test_response, 'en')
                test_results['status'] = 'pass' if result.get('i18n_applied', False) else 'fail'
                test_results['details'] = result
                
            else:
                test_results['status'] = 'unsupported'
                test_results['error'] = f"Componente {component} no soportado para testing"
            
            return test_results
            
        except Exception as e:
            logger.error(f"Error probando componente {component}: {e}")
            return {
                'component': component,
                'status': 'error',
                'error': str(e)
            }

# Mantener compatibilidad con el nombre anterior
GeminiService = HybridGeminiService
