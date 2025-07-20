from flask import Blueprint, request, jsonify
from ..services.gemini_service import GeminiService
import logging

logger = logging.getLogger(__name__)

# Crear blueprint
chat_bp = Blueprint('chat', __name__)

# Inicializar servicio
gemini_service = GeminiService()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal para el chat"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Mensaje requerido'
            }), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({
                'error': 'Mensaje no puede estar vacío'
            }), 400
        
        user_context = data.get('context')  # Contexto opcional del usuario
        
        # Generar respuesta
        result = gemini_service.generate_response(message, user_context)
        
        return jsonify({
            'response': result['response'],
            'metadata': {
                'sources_used': result.get('sources_used', 0),
                'context_found': result.get('context_found', False)
            }
        })
        
    except Exception as e:
        logger.error(f"Error en endpoint /chat: {e}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

@chat_bp.route('/chat/status', methods=['GET'])
def chat_status():
    """Endpoint para verificar el estado del sistema"""
    try:
        status = gemini_service.get_system_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error en endpoint /status: {e}")
        return jsonify({
            'error': 'Error obteniendo estado del sistema'
        }), 500

@chat_bp.route('/chat/reload-documents', methods=['POST'])
def reload_documents():
    """Endpoint para recargar documentos"""
    try:
        result = gemini_service.reload_documents()
        
        if result['success']:
            return jsonify({
                'message': result['message']
            })
        else:
            return jsonify({
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error en endpoint /reload-documents: {e}")
        return jsonify({
            'error': 'Error recargando documentos'
        }), 500

@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'portfolio-chatbot-api'
    })

# Manejo de errores
@chat_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint no encontrado'
    }), 404

@chat_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Método no permitido'
    }), 405