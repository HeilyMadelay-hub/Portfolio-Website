import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from ..utils.faq_checker import faq_classifier

logger = logging.getLogger(__name__)

@dataclass
class EmergencyResponse:
    """Respuesta de emergencia predefinida"""
    message: str
    category: str
    confidence: float = 1.0

class EmergencyMode:
    """
    Modo de emergencia según diagrama híbrido
    SERVICE_STATUS -> No -> EMERGENCY (Solo FAQs)
    """
    
    def __init__(self):
        self.is_active = False
        self.activation_reason = ""
        self.emergency_responses = self._load_emergency_responses()
        
        logger.info("EmergencyMode inicializado")
    
    def activate(self, reason: str = "Servicios externos no disponibles"):
        """Activa el modo de emergencia"""
        self.is_active = True
        self.activation_reason = reason
        logger.warning(f"Modo de emergencia ACTIVADO: {reason}")
    
    def deactivate(self):
        """Desactiva el modo de emergencia"""
        self.is_active = False
        self.activation_reason = ""
        logger.info("Modo de emergencia DESACTIVADO")
    
    def handle_emergency_request(self, message: str) -> Dict[str, any]:
        """
        Maneja requests en modo de emergencia (solo FAQs)
        
        Args:
            message: Mensaje del usuario
        
        Returns:
            Dict con respuesta de emergencia
        """
        try:
            if not self.is_active:
                return {
                    'is_emergency': False,
                    'message': 'Modo de emergencia no está activo'
                }
            
            # Intentar clasificar como FAQ primero
            faq_result = faq_classifier.classify_message(message)
            
            if faq_result.get('is_faq', False):
                return {
                    'is_emergency': True,
                    'response': faq_result['response'],
                    'source': 'faq',
                    'confidence': faq_result['confidence'],
                    'category': faq_result.get('category', 'general'),
                    'emergency_reason': self.activation_reason
                }
            
            # Si no es FAQ, usar respuestas de emergencia predefinidas
            emergency_response = self._get_emergency_response(message)
            
            return {
                'is_emergency': True,
                'response': emergency_response.message,
                'source': 'emergency_template',
                'confidence': emergency_response.confidence,
                'category': emergency_response.category,
                'emergency_reason': self.activation_reason,
                'limitation_notice': True
            }
            
        except Exception as e:
            logger.error(f"Error en modo de emergencia: {e}")
            return {
                'is_emergency': True,
                'response': self._get_critical_fallback_response(),
                'source': 'critical_fallback',
                'confidence': 1.0,
                'category': 'error',
                'error': str(e)
            }
    
    def _load_emergency_responses(self) -> List[EmergencyResponse]:
        """Carga respuestas de emergencia predefinidas"""
        return [
            EmergencyResponse(
                message="Actualmente tengo problemas técnicos con mis servicios principales. Puedo ayudarte con información básica sobre mi perfil profesional. Mi experiencia incluye desarrollo full-stack con React, Python y tecnologías modernas.",
                category="experiencia",
                confidence=0.8
            ),
            
            EmergencyResponse(
                message="Debido a problemas técnicos temporales, mi capacidad de respuesta está limitada. Para información de contacto, puedes buscarme en LinkedIn o enviar un email a través de mi perfil profesional.",
                category="contacto",
                confidence=0.8
            ),
            
            EmergencyResponse(
                message="Mis servicios de IA están temporalmente fuera de línea. Te puedo decir que trabajo con tecnologías como React, Python, Flask, Node.js, bases de datos y servicios de cloud.",
                category="tecnologias",
                confidence=0.8
            ),
            
            EmergencyResponse(
                message="Actualmente hay problemas técnicos que limitan mis respuestas detalladas. He desarrollado varios proyectos incluyendo aplicaciones web, chatbots con IA y sistemas de gestión de datos.",
                category="proyectos",
                confidence=0.8
            ),
            
            EmergencyResponse(
                message="Por problemas técnicos temporales, solo puedo dar respuestas básicas. Sí estoy disponible para oportunidades laborales como desarrollador full-stack.",
                category="disponibilidad",
                confidence=0.8
            ),
            
            EmergencyResponse(
                message="Lo siento, actualmente tengo problemas técnicos que afectan mi capacidad de dar respuestas detalladas. Por favor intenta de nuevo más tarde o contacta directamente para información específica.",
                category="general",
                confidence=0.6
            )
        ]
    
    def _get_emergency_response(self, message: str) -> EmergencyResponse:
        """Selecciona la mejor respuesta de emergencia para el mensaje"""
        message_lower = message.lower()
        
        # Keywords para categorización
        category_keywords = {
            "experiencia": ["experiencia", "trabajo", "laboral", "años", "profesional"],
            "contacto": ["contacto", "email", "linkedin", "telefono", "ubicar"],
            "tecnologias": ["tecnologías", "lenguajes", "frameworks", "stack", "programación"],
            "proyectos": ["proyectos", "portfolio", "desarrollado", "construido"],
            "disponibilidad": ["disponible", "trabajo", "empleo", "contratar", "busco"],
        }
        
        # Encontrar categoría más relevante
        best_category = "general"
        max_matches = 0
        
        for category, keywords in category_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        # Buscar respuesta para la categoría
        for response in self.emergency_responses:
            if response.category == best_category:
                return response
        
        # Fallback a respuesta general
        return next(
            (r for r in self.emergency_responses if r.category == "general"),
            self.emergency_responses[-1]  # Última respuesta como fallback final
        )
    
    def _get_critical_fallback_response(self) -> str:
        """Respuesta crítica cuando todo falla"""
        return "Disculpa, estoy experimentando problemas técnicos serios. Por favor intenta contactar directamente para obtener información sobre mi perfil profesional."
    
    def check_services_health(self, llm_available: bool, vector_store_available: bool, embedding_available: bool) -> bool:
        """
        Verifica la salud de los servicios y activa/desactiva emergencia
        
        Args:
            llm_available: Si el LLM está disponible
            vector_store_available: Si el vector store está disponible  
            embedding_available: Si los embeddings están disponibles
        
        Returns:
            True si los servicios están OK, False si se debe activar emergencia
        """
        try:
            # Criterios para activar modo de emergencia
            critical_services_down = 0
            issues = []
            
            if not llm_available:
                critical_services_down += 1
                issues.append("LLM no disponible")
            
            if not vector_store_available:
                critical_services_down += 1
                issues.append("Vector store no disponible")
            
            if not embedding_available:
                critical_services_down += 1
                issues.append("Embeddings no disponibles")
            
            # Activar emergencia si 2 o más servicios críticos fallan
            should_activate_emergency = critical_services_down >= 2
            
            if should_activate_emergency and not self.is_active:
                reason = f"Servicios críticos fallaron: {', '.join(issues)}"
                self.activate(reason)
                return False
            elif not should_activate_emergency and self.is_active:
                self.deactivate()
                return True
            
            return not should_activate_emergency
            
        except Exception as e:
            logger.error(f"Error verificando salud de servicios: {e}")
            # En caso de error, activar emergencia por seguridad
            if not self.is_active:
                self.activate(f"Error verificando servicios: {str(e)}")
            return False
    
    def get_status(self) -> Dict[str, any]:
        """Estado del modo de emergencia"""
        return {
            'is_active': self.is_active,
            'activation_reason': self.activation_reason,
            'emergency_responses_count': len(self.emergency_responses),
            'faq_fallback_available': faq_classifier is not None
        }
    
    def simulate_emergency(self, reason: str = "Simulación de emergencia"):
        """Simula activación de emergencia (para testing)"""
        self.activate(reason)
        logger.info(f"Emergencia simulada: {reason}")
    
    def get_emergency_stats(self) -> Dict[str, any]:
        """Estadísticas del modo de emergencia"""
        categories = {}
        for response in self.emergency_responses:
            categories[response.category] = categories.get(response.category, 0) + 1
        
        return {
            'total_emergency_responses': len(self.emergency_responses),
            'categories': categories,
            'current_status': 'active' if self.is_active else 'inactive',
            'last_activation_reason': self.activation_reason if self.is_active else None
        }

# Instancia global del modo de emergencia
emergency_mode = EmergencyMode()

def handle_emergency(message: str) -> Dict[str, any]:
    """Función helper para manejo de emergencias"""
    return emergency_mode.handle_emergency_request(message)

def check_emergency_activation(llm_ok: bool, vector_ok: bool, embedding_ok: bool) -> bool:
    """Función helper para verificar activación de emergencia"""
    return emergency_mode.check_services_health(llm_ok, vector_ok, embedding_ok)

def is_emergency_active() -> bool:
    """Verifica si el modo de emergencia está activo"""
    return emergency_mode.is_active
