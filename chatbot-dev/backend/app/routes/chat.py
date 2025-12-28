"""
Chat Routes con integración completa del flujo híbrido
Implementa el diagrama completo: Rate Limiting -> Processing -> Response
Soporta tanto FastAPI como Flask
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
import time

# Compatibilidad con FastAPI y Flask
try:
    from fastapi import APIRouter, Request, HTTPException, status, Depends
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    USE_FASTAPI = True
except ImportError:
    from flask import Blueprint, request, jsonify
    USE_FASTAPI = False

from ..core.orchestrator import HybridRAGOrchestrator
from ..middleware.rate_limit_middleware import require_rate_limit
from ..utils.rate_limiter import get_client_identifier
from ..services.emergency_mode import emergency_mode
from ..services.i18n_service import i18n_service
from ..config.settings import Config

logger = logging.getLogger(__name__)

# ==================== MODELOS PYDANTIC (FastAPI) ====================
if USE_FASTAPI:
    class ChatRequest(BaseModel):
        message: str
        context: Optional[str] = None
        language: Optional[str] = "es"
        session_id: Optional[str] = None
    
    class ChatResponse(BaseModel):
        success: bool
        response: str
        metadata: Dict[str, Any]
        rate_limit: Optional[Dict[str, Any]] = None
        guidance: Optional[bool] = False
        question_templates: Optional[list] = []
        clarification_needed: Optional[bool] = False
        conflicting_sections: Optional[list] = []
        retry_after: Optional[int] = None
    
    class EmergencySimulateRequest(BaseModel):
        reason: Optional[str] = "Simulación manual de emergencia"
        duration: Optional[int] = 60  # segundos

# ==================== INICIALIZACIÓN ====================

# Inicializar orquestador híbrido una sola vez
orchestrator = HybridRAGOrchestrator()

# ==================== IMPLEMENTACIÓN FASTAPI ====================
if USE_FASTAPI:
    router = APIRouter(prefix="/api", tags=["chat"])
    
    @router.post("/chat", response_model=ChatResponse)
    @require_rate_limit(limit=60, window=3600, category="chat")
    async def chat_endpoint(request: Request, chat_request: ChatRequest):
        """
        Endpoint principal para el chat híbrido con flujo completo del diagrama
        
        Flujo: Rate Limiting -> Input Processing -> Cache -> Health Check -> 
               Section Validation -> FAQ -> RAG -> Safety -> i18n -> Response
        """
        try:
            # Obtener identificador del cliente para rate limiting
            client_id = get_client_identifier(request)
            
            # Extraer información del request
            user_language = request.headers.get('Accept-Language', chat_request.language).split(',')[0][:2]
            
            # Procesar usando orquestador híbrido con flujo completo
            result = orchestrator.process_hybrid_request(
                message=chat_request.message,
                client_identifier=client_id,
                user_context=chat_request.context,
                target_language=user_language
            )
            
            # Determinar código de estado
            if not result.get('success', False):
                if 'rate_limit_exceeded' in result.get('metadata', {}).get('flow_path', []):
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=result
                    )
                elif 'input_validation_failed' in result.get('metadata', {}).get('flow_path', []):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=result
                    )
            
            # Agregar información de rate limiting desde el state
            if hasattr(request.state, 'rate_limit_info'):
                result['rate_limit'] = {
                    'limit': request.state.rate_limit_info.get('limit'),
                    'remaining': request.state.rate_limit_info.get('remaining'),
                    'reset': request.state.rate_limit_info.get('reset_at')
                }
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en endpoint /chat híbrido: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    'success': False,
                    'error': 'Error interno del servidor',
                    'flow_path': ['critical_error']
                }
            )
    
    @router.get("/chat/status")
    async def chat_status():
        """Estado completo del sistema híbrido con todos los componentes"""
        try:
            status = orchestrator.get_system_status()
            return status
        except Exception as e:
            logger.error(f"Error obteniendo estado: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'error': str(e)}
            )
    
    @router.get("/chat/health")
    async def health_check():
        """Health check rápido del sistema híbrido"""
        try:
            services_health = orchestrator._check_services_health()
            is_healthy = all([
                services_health.get('llm_available', False),
                services_health.get('documents_initialized', False)
            ])
            
            response = {
                'healthy': is_healthy,
                'timestamp': datetime.now().isoformat(),
                'services': services_health,
                'emergency_mode': emergency_mode.is_active
            }
            
            if not is_healthy:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=response
                )
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={'healthy': False, 'error': str(e)}
            )
    
    @router.post("/chat/reload-documents")
    @require_rate_limit(limit=10, window=3600, category="admin")
    async def reload_documents(request: Request):
        """Recarga documentos en el sistema híbrido (protegido por API key admin)"""
        # Validar API Key
        api_key = request.headers.get('X-API-Key')
        if not Config.is_valid_admin_key(api_key):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'admin_api_key_required'})

        try:
            result = orchestrator.reload_documents()
            
            if not result.get('success', False):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error recargando documentos: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'success': False, 'error': str(e)}
            )
    
    @router.get("/chat/emergency/status")
    async def emergency_status():
        """Estado del modo de emergencia"""
        return emergency_mode.get_status()
    
    @router.post("/chat/emergency/simulate")
    @require_rate_limit(limit=5, window=3600, category="admin")
    async def simulate_emergency(request: Request, emergency_request: EmergencySimulateRequest):
        """Simula modo de emergencia para testing (protegido por API key admin)"""
        api_key = request.headers.get('X-API-Key')
        if not Config.is_valid_admin_key(api_key):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'admin_api_key_required'})
        try:
            emergency_mode.simulate_emergency(
                emergency_request.reason,
                emergency_request.duration
            )
            
            return {
                'success': True,
                'message': 'Modo de emergencia activado',
                'reason': emergency_request.reason,
                'duration': emergency_request.duration
            }
        except Exception as e:
            logger.error(f"Error simulando emergencia: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'error': str(e)}
            )
    
    @router.post("/chat/emergency/deactivate")
    @require_rate_limit(limit=5, window=3600, category="admin")
    async def deactivate_emergency(request: Request):
        """Desactiva modo de emergencia (protegido por API key admin)"""
        api_key = request.headers.get('X-API-Key')
        if not Config.is_valid_admin_key(api_key):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'admin_api_key_required'})
        try:
            emergency_mode.deactivate()
            return {
                'success': True,
                'message': 'Modo de emergencia desactivado'
            }
        except Exception as e:
            logger.error(f"Error desactivando emergencia: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={'error': str(e)}
            )
    
    @router.get("/chat/languages")
    async def supported_languages():
        """Idiomas soportados por el sistema"""
        return {
            'supported_languages': i18n_service.get_supported_languages(),
            'default_language': 'es',
            'auto_detection': True
        }

# ==================== IMPLEMENTACIÓN FLASK (Compatibilidad) ====================
else:
    chat_bp = Blueprint('chat', __name__)
    
    @chat_bp.route('/api/chat', methods=['POST'])
    def chat():
        """Endpoint principal para el chat híbrido (Flask)"""
        try:
            data = request.get_json()
            
            if not data or 'message' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Mensaje requerido',
                    'flow_path': ['input_validation_failed']
                }), 400
            
            # Obtener identificador del cliente
            client_id = get_client_identifier(request)
            
            # Extraer parámetros
            message = data.get('message', '').strip()
            user_context = data.get('context')
            target_language = data.get('language', 'es')
            
            # Procesar usando orquestador híbrido
            result = orchestrator.process_hybrid_request(
                message=message,
                client_identifier=client_id,
                user_context=user_context,
                target_language=target_language
            )
            
            # Determinar código de estado
            if result.get('success', False):
                status_code = 200
            elif 'rate_limit_exceeded' in result.get('metadata', {}).get('flow_path', []):
                status_code = 429
            elif 'input_validation_failed' in result.get('metadata', {}).get('flow_path', []):
                status_code = 400
            else:
                status_code = 500
            
            return jsonify(result), status_code
            
        except Exception as e:
            logger.error(f"Error en endpoint /chat híbrido: {e}")
            return jsonify({
                'success': False,
                'error': 'Error interno del servidor',
                'flow_path': ['critical_error']
            }), 500
    
    @chat_bp.route('/api/chat/status', methods=['GET'])
    def chat_status():
        """Estado del sistema híbrido (Flask)"""
        try:
            status = orchestrator.get_system_status()
            return jsonify(status)
        except Exception as e:
            logger.error(f"Error obteniendo estado: {e}")
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/api/chat/health', methods=['GET'])
    def health_check():
        """Health check (Flask)"""
        try:
            services_health = orchestrator._check_services_health()
            is_healthy = all([
                services_health.get('llm_available', False),
                services_health.get('documents_initialized', False)
            ])
            
            response = {
                'healthy': is_healthy,
                'timestamp': datetime.now().isoformat(),
                'services': services_health,
                'emergency_mode': emergency_mode.is_active
            }
            
            status_code = 200 if is_healthy else 503
            return jsonify(response), status_code
            
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return jsonify({'healthy': False, 'error': str(e)}), 503
    
    @chat_bp.route('/api/chat/reload-documents', methods=['POST'])
    def reload_documents():
        """Recarga documentos (Flask)"""
        try:
            # Validar API Key desde headers o args
            api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
            if not Config.is_valid_admin_key(api_key):
                return jsonify({'error': 'admin_api_key_required'}), 403
            
            result = orchestrator.reload_documents()
            status_code = 200 if result.get('success', False) else 500
            return jsonify(result), status_code
        except Exception as e:
            logger.error(f"Error recargando documentos: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @chat_bp.route('/api/chat/emergency/status', methods=['GET'])
    def emergency_status():
        """Estado del modo de emergencia (Flask)"""
        return jsonify(emergency_mode.get_status())
    
    @chat_bp.route('/api/chat/emergency/simulate', methods=['POST'])
    def simulate_emergency():
        """Simula modo de emergencia (Flask)"""
        try:
            data = request.get_json() if request.is_json else {}
            reason = data.get('reason', 'Simulación manual')
            duration = data.get('duration', 60)
            
            # Validar API Key desde headers o args
            api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
            if not Config.is_valid_admin_key(api_key):
                return jsonify({'error': 'admin_api_key_required'}), 403
            
            emergency_mode.simulate_emergency(reason, duration)
            
            return jsonify({
                'success': True,
                'message': 'Modo de emergencia activado',
                'reason': reason,
                'duration': duration
            })
        except Exception as e:
            logger.error(f"Error simulando emergencia: {e}")
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/api/chat/emergency/deactivate', methods=['POST'])
    def deactivate_emergency():
        """Desactiva modo de emergencia (Flask)"""
        try:
            # Validar API Key desde headers o args
            api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
            if not Config.is_valid_admin_key(api_key):
                return jsonify({'error': 'admin_api_key_required'}), 403
            
            emergency_mode.deactivate()
            return jsonify({
                'success': True,
                'message': 'Modo de emergencia desactivado'
            })
        except Exception as e:
            logger.error(f"Error desactivando emergencia: {e}")
            return jsonify({'error': str(e)}), 500
    
    @chat_bp.route('/api/chat/languages', methods=['GET'])
    def supported_languages():
        """Idiomas soportados (Flask)"""
        return jsonify({
            'supported_languages': i18n_service.get_supported_languages(),
            'default_language': 'es',
            'auto_detection': True
        })
    
    # Exportar blueprint para Flask
    router = chat_bp

# ==================== FUNCIONES DE UTILIDAD ====================

def get_flow_analytics() -> Dict[str, Any]:
    """
    Obtiene analíticas del flujo de procesamiento
    """
    # TODO: Implementar analíticas detalladas
    return {
        'total_requests': 0,
        'flow_paths': {},
        'average_processing_time': {},
        'cache_hit_rate': 0,
        'faq_hit_rate': 0,
        'emergency_activations': 0
    }

def test_flow_component(component: str, test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Prueba un componente específico del flujo
    
    Args:
        component: Nombre del componente a probar
        test_data: Datos de prueba opcionales
    
    Returns:
        Resultado del test
    """
    components_map = {
        'rate_limiter': lambda: test_rate_limiter(test_data),
        'input_processor': lambda: test_input_processor(test_data),
        'faq_classifier': lambda: test_faq_classifier(test_data),
        'section_validator': lambda: test_section_validator(test_data),
        'safety_checker': lambda: test_safety_checker(test_data),
        'i18n_service': lambda: test_i18n_service(test_data),
        'cache': lambda: test_cache(test_data),
        'emergency_mode': lambda: test_emergency_mode(test_data)
    }
    
    if component not in components_map:
        return {
            'component': component,
            'status': 'error',
            'error': f'Componente {component} no encontrado'
        }
    
    try:
        result = components_map[component]()
        return {
            'component': component,
            'status': 'pass' if result.get('success', False) else 'fail',
            'details': result
        }
    except Exception as e:
        return {
            'component': component,
            'status': 'error',
            'error': str(e)
        }

# ==================== FUNCIONES DE TEST DE COMPONENTES ====================

def test_rate_limiter(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el rate limiter"""
    from ..utils.rate_limiter import check_rate_limit
    
    test_client = test_data.get('client_id', 'test_client') if test_data else 'test_client'
    result = check_rate_limit(test_client, 'test')
    
    return {
        'success': True,
        'allowed': result.get('allowed'),
        'remaining': result.get('remaining'),
        'limit': result.get('limit')
    }

def test_input_processor(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el procesador de entrada"""
    from ..utils.sanitizer import process_user_input
    
    test_message = test_data.get('message', 'Test message') if test_data else 'Test message'
    result = process_user_input(test_message)
    
    return {
        'success': result.get('is_valid', False),
        'processed_message': result.get('processed_message'),
        'warnings': result.get('warnings', [])
    }

def test_faq_classifier(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el clasificador FAQ"""
    from ..utils.faq_checker import classify_user_message
    
    test_message = test_data.get('message', '¿Cuál es tu experiencia?') if test_data else '¿Cuál es tu experiencia?'
    result = classify_user_message(test_message)
    
    return {
        'success': True,
        'is_faq': result.get('is_faq'),
        'confidence': result.get('confidence'),
        'category': result.get('category')
    }

def test_section_validator(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el validador de sección"""
    from ..utils.section_templates import validate_message_section
    
    test_message = test_data.get('message', 'Háblame sobre proyectos') if test_data else 'Háblame sobre proyectos'
    result = validate_message_section(test_message)
    
    return {
        'success': result.get('is_valid', False),
        'detected_section': result.get('detected_section'),
        'confidence': result.get('confidence')
    }

def test_safety_checker(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el verificador de seguridad"""
    from ..services.safety_checker import check_input_safety
    
    test_message = test_data.get('message', 'Test seguro') if test_data else 'Test seguro'
    result = check_input_safety(test_message)
    
    return {
        'success': result.get('is_safe', False),
        'issues': result.get('issues', [])
    }

def test_i18n_service(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el servicio i18n"""
    from ..services.i18n_service import detect_user_language, translate_response
    
    test_message = test_data.get('message', 'Hello, how are you?') if test_data else 'Hello, how are you?'
    detected_lang = detect_user_language(test_message)
    
    test_response = {'response': 'Esta es una respuesta de prueba'}
    translated = translate_response(test_response, 'en')
    
    return {
        'success': True,
        'detected_language': detected_lang,
        'translation_applied': translated.get('i18n_applied', False)
    }

def test_cache(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el sistema de cache"""
    try:
        test_key = test_data.get('key', 'test_key') if test_data else 'test_key'
        test_value = test_data.get('value', {'test': 'data'}) if test_data else {'test': 'data'}
        
        # Probar set y get
        orchestrator.cache_provider.set(test_key, test_value, ttl=60)
        retrieved = orchestrator.cache_provider.get(test_key)
        
        success = retrieved == test_value
        
        # Limpiar
        orchestrator.cache_provider.delete(test_key)
        
        return {
            'success': success,
            'stored': test_value,
            'retrieved': retrieved
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def test_emergency_mode(test_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Prueba el modo de emergencia"""
    from ..services.emergency_mode import emergency_mode, handle_emergency
    
    # Simular emergencia temporalmente
    was_active = emergency_mode.is_active
    emergency_mode.simulate_emergency("Test", 1)
    
    test_message = test_data.get('message', 'Test de emergencia') if test_data else 'Test de emergencia'
    response = handle_emergency(test_message)
    
    # Restaurar estado
    if not was_active:
        emergency_mode.deactivate()
    
    return {
        'success': bool(response),
        'emergency_response': response,
        'templates_available': len(emergency_mode.emergency_responses) > 0
    }

# ==================== EXPORTACIÓN ====================

# Exportar router para ser usado por la aplicación principal
__all__ = ['router', 'orchestrator', 'get_flow_analytics', 'test_flow_component']
