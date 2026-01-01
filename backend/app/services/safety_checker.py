import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class SafetyLevel(Enum):
    """Niveles de seguridad"""
    SAFE = "safe"
    WARNING = "warning"
    UNSAFE = "unsafe"
    BLOCKED = "blocked"

@dataclass
class SafetyRule:
    """Regla de seguridad"""
    id: str
    pattern: str
    level: SafetyLevel
    category: str
    description: str
    action: str  # block, warn, filter, template

class SafetyChecker:
    """
    Verificador de seguridad según diagrama híbrido
    GEMINI_FLASH -> SAFETY_CHECK -> RESP_STRUCT/TEMPLATE_RESP
    """
    
    def __init__(self):
        self.safety_rules: Dict[str, SafetyRule] = {}
        self.blocked_patterns: List[re.Pattern] = []
        self.warning_patterns: List[re.Pattern] = []
        
        # Cargar reglas de seguridad
        self._load_safety_rules()
        self._compile_patterns()
        
        logger.info(f"SafetyChecker inicializado con {len(self.safety_rules)} reglas")
    
    def check_input_safety(self, message: str) -> Dict[str, any]:
        """
        Verifica seguridad del input del usuario
        
        Args:
            message: Mensaje del usuario
        
        Returns:
            Dict con is_safe, level, issues, filtered_message
        """
        try:
            issues = []
            filtered_message = message
            max_level = SafetyLevel.SAFE
            
            # Verificar cada regla de seguridad
            for rule_id, rule in self.safety_rules.items():
                if self._matches_pattern(message, rule.pattern):
                    issues.append({
                        'rule_id': rule_id,
                        'category': rule.category,
                        'level': rule.level.value,
                        'description': rule.description,
                        'action': rule.action
                    })
                    
                    # Actualizar nivel máximo de riesgo
                    if self._is_more_severe(rule.level, max_level):
                        max_level = rule.level
                    
                    # Aplicar acción correspondiente
                    if rule.action == "filter":
                        filtered_message = self._apply_filter(filtered_message, rule.pattern)
                    elif rule.action == "block":
                        filtered_message = ""
                        break
            
            return {
                'is_safe': max_level in [SafetyLevel.SAFE, SafetyLevel.WARNING],
                'level': max_level.value,
                'issues': issues,
                'filtered_message': filtered_message,
                'original_length': len(message),
                'filtered_length': len(filtered_message)
            }
            
        except Exception as e:
            logger.error(f"Error verificando seguridad del input: {e}")
            return {
                'is_safe': True,  # Fail-safe por defecto
                'level': SafetyLevel.SAFE.value,
                'issues': [],
                'filtered_message': message,
                'error': str(e)
            }
    
    def check_output_safety(self, response: str, context: Dict = None) -> Dict[str, any]:
        """
        Verifica seguridad de la respuesta generada por Gemini
        
        Args:
            response: Respuesta generada
            context: Contexto adicional
        
        Returns:
            Dict con is_safe, issues, safe_response
        """
        try:
            issues = []
            safe_response = response
            max_level = SafetyLevel.SAFE
            
            # Verificar contenido inapropiado en la respuesta
            output_issues = self._check_output_content(response)
            issues.extend(output_issues)
            
            # Verificar coherencia con el contexto
            if context:
                coherence_issues = self._check_response_coherence(response, context)
                issues.extend(coherence_issues)
            
            # Determinar nivel de seguridad
            if issues:
                severity_levels = [issue['level'] for issue in issues]
                if 'blocked' in severity_levels:
                    max_level = SafetyLevel.BLOCKED
                elif 'unsafe' in severity_levels:
                    max_level = SafetyLevel.UNSAFE
                elif 'warning' in severity_levels:
                    max_level = SafetyLevel.WARNING
            
            # Aplicar filtros o generar respuesta segura
            if max_level == SafetyLevel.BLOCKED:
                safe_response = self._get_template_response("blocked")
            elif max_level == SafetyLevel.UNSAFE:
                safe_response = self._get_template_response("unsafe")
            elif max_level == SafetyLevel.WARNING:
                safe_response = self._apply_output_filters(response)
            
            return {
                'is_safe': max_level in [SafetyLevel.SAFE, SafetyLevel.WARNING],
                'level': max_level.value,
                'issues': issues,
                'safe_response': safe_response,
                'original_response': response,
                'was_filtered': safe_response != response
            }
            
        except Exception as e:
            logger.error(f"Error verificando seguridad del output: {e}")
            return {
                'is_safe': False,
                'level': SafetyLevel.UNSAFE.value,
                'issues': [{'category': 'error', 'description': str(e)}],
                'safe_response': self._get_template_response("error"),
                'error': str(e)
            }
    
    def _load_safety_rules(self):
        """Carga reglas de seguridad predefinidas"""
        rules = [
            # Contenido inapropiado
            SafetyRule(
                id="inappropriate_content",
                pattern=r"(sexo|drogas|violencia|odio|discriminación)",
                level=SafetyLevel.BLOCKED,
                category="contenido_inapropiado",
                description="Contenido inapropiado detectado",
                action="block"
            ),
            
            # Información personal sensible
            SafetyRule(
                id="personal_info",
                pattern=r"(\d{3}-\d{2}-\d{4}|\d{16}|password|contraseña)",
                level=SafetyLevel.UNSAFE,
                category="informacion_personal",
                description="Posible información personal sensible",
                action="filter"
            ),
            
            # Lenguaje ofensivo
            SafetyRule(
                id="offensive_language",
                pattern=r"(idiota|estúpido|maldito|carajo)",
                level=SafetyLevel.WARNING,
                category="lenguaje_ofensivo",
                description="Lenguaje potencialmente ofensivo",
                action="warn"
            ),
            
            # Solicitudes de información no autorizada
            SafetyRule(
                id="unauthorized_requests",
                pattern=r"(hackear|crackear|piratear|robar|contraseña)",
                level=SafetyLevel.BLOCKED,
                category="solicitud_no_autorizada",
                description="Solicitud no autorizada detectada",
                action="block"
            ),
            
            # Spam o contenido repetitivo
            SafetyRule(
                id="spam_content",
                pattern=r"(.)\1{10,}",  # Más de 10 caracteres repetidos
                level=SafetyLevel.WARNING,
                category="spam",
                description="Posible spam detectado",
                action="filter"
            ),
            
            # URLs sospechosas
            SafetyRule(
                id="suspicious_urls",
                pattern=r"(bit\.ly|tinyurl|goo\.gl)/\w+",
                level=SafetyLevel.WARNING,
                category="url_sospechosa",
                description="URL acortada detectada",
                action="warn"
            ),
            
            # Código malicioso
            SafetyRule(
                id="malicious_code",
                pattern=r"(eval\(|exec\(|<script|javascript:)",
                level=SafetyLevel.BLOCKED,
                category="codigo_malicioso",
                description="Código potencialmente malicioso",
                action="block"
            )
        ]
        
        # Cargar reglas al diccionario
        for rule in rules:
            self.safety_rules[rule.id] = rule
    
    def _compile_patterns(self):
        """Compila patrones regex para optimización"""
        self.blocked_patterns = []
        self.warning_patterns = []
        
        for rule in self.safety_rules.values():
            try:
                compiled_pattern = re.compile(rule.pattern, re.IGNORECASE)
                
                if rule.level == SafetyLevel.BLOCKED:
                    self.blocked_patterns.append(compiled_pattern)
                elif rule.level in [SafetyLevel.WARNING, SafetyLevel.UNSAFE]:
                    self.warning_patterns.append(compiled_pattern)
                    
            except re.error as e:
                logger.warning(f"Patrón regex inválido en regla {rule.id}: {e}")
    
    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """Verifica si el texto coincide con el patrón"""
        try:
            return bool(re.search(pattern, text, re.IGNORECASE))
        except re.error:
            return False
    
    def _is_more_severe(self, level1: SafetyLevel, level2: SafetyLevel) -> bool:
        """Compara severidad de niveles de seguridad"""
        severity_order = {
            SafetyLevel.SAFE: 0,
            SafetyLevel.WARNING: 1,
            SafetyLevel.UNSAFE: 2,
            SafetyLevel.BLOCKED: 3
        }
        return severity_order[level1] > severity_order[level2]
    
    def _apply_filter(self, text: str, pattern: str) -> str:
        """Aplica filtro para remover contenido problemático"""
        try:
            return re.sub(pattern, "[FILTRADO]", text, flags=re.IGNORECASE)
        except re.error:
            return text
    
    def _check_output_content(self, response: str) -> List[Dict]:
        """Verifica contenido de la respuesta"""
        issues = []
        
        # Verificar longitud excesiva
        if len(response) > 2000:
            issues.append({
                'category': 'longitud_excesiva',
                'level': 'warning',
                'description': 'Respuesta muy larga'
            })
        
        # Verificar repetición excesiva
        words = response.split()
        if len(words) > 10:
            unique_words = set(words)
            repetition_ratio = len(words) / len(unique_words)
            if repetition_ratio > 3:
                issues.append({
                    'category': 'repeticion_excesiva',
                    'level': 'warning',
                    'description': 'Contenido muy repetitivo'
                })
        
        # Verificar contenido vacío o sin sentido
        if len(response.strip()) < 10:
            issues.append({
                'category': 'contenido_insuficiente',
                'level': 'unsafe',
                'description': 'Respuesta muy corta o vacía'
            })
        
        return issues
    
    def _check_response_coherence(self, response: str, context: Dict) -> List[Dict]:
        """Verifica coherencia de la respuesta con el contexto"""
        issues = []
        
        # Verificar si la respuesta está relacionada con el contexto
        if 'user_message' in context:
            user_message = context['user_message'].lower()
            response_lower = response.lower()
            
            # Verificar si hay alguna relación temática básica
            common_words = set(user_message.split()) & set(response_lower.split())
            if len(common_words) < 2 and len(user_message.split()) > 3:
                issues.append({
                    'category': 'coherencia_baja',
                    'level': 'warning',
                    'description': 'Respuesta poco relacionada con la pregunta'
                })
        
        return issues
    
    def _apply_output_filters(self, response: str) -> str:
        """Aplica filtros de seguridad a la respuesta"""
        filtered = response
        
        # Filtrar URLs sospechosas
        filtered = re.sub(
            r'(bit\.ly|tinyurl|goo\.gl)/\w+', 
            '[URL_FILTRADA]', 
            filtered, 
            flags=re.IGNORECASE
        )
        
        # Filtrar repeticiones excesivas
        filtered = re.sub(r'(.)\1{5,}', r'\1\1\1', filtered)
        
        return filtered
    
    def _get_template_response(self, response_type: str) -> str:
        """Obtiene respuesta plantilla para casos inseguros"""
        templates = {
            "blocked": "Lo siento, no puedo procesar ese tipo de solicitud. Por favor, haz una pregunta relacionada con mi perfil profesional.",
            "unsafe": "Hay un problema con la respuesta generada. Por favor, intenta reformular tu pregunta sobre mi experiencia o habilidades.",
            "error": "Ocurrió un error al generar la respuesta. Por favor, intenta de nuevo con una pregunta sobre mi perfil profesional.",
            "inappropriate": "No puedo proporcionar información sobre ese tema. ¿Te gustaría saber sobre mi experiencia profesional o proyectos?"
        }
        
        return templates.get(response_type, templates["error"])
    
    def add_safety_rule(self, rule: SafetyRule) -> bool:
        """Agrega nueva regla de seguridad"""
        try:
            # Verificar que el patrón sea válido
            re.compile(rule.pattern)
            
            self.safety_rules[rule.id] = rule
            self._compile_patterns()
            
            logger.info(f"Regla de seguridad agregada: {rule.id}")
            return True
        except re.error as e:
            logger.error(f"Error agregando regla {rule.id}: Patrón inválido - {e}")
            return False
        except Exception as e:
            logger.error(f"Error agregando regla {rule.id}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, any]:
        """Estadísticas del verificador de seguridad"""
        level_counts = {}
        category_counts = {}
        
        for rule in self.safety_rules.values():
            level_counts[rule.level.value] = level_counts.get(rule.level.value, 0) + 1
            category_counts[rule.category] = category_counts.get(rule.category, 0) + 1
        
        return {
            'total_rules': len(self.safety_rules),
            'by_level': level_counts,
            'by_category': category_counts,
            'blocked_patterns': len(self.blocked_patterns),
            'warning_patterns': len(self.warning_patterns)
        }

# Instancia global del verificador de seguridad
safety_checker = SafetyChecker()

def check_input_safety(message: str) -> Dict[str, any]:
    """Función helper para verificar seguridad del input"""
    return safety_checker.check_input_safety(message)

def check_output_safety(response: str, context: Dict = None) -> Dict[str, any]:
    """Función helper para verificar seguridad del output"""
    return safety_checker.check_output_safety(response, context)

def is_safe_content(text: str) -> bool:
    """Verificación rápida de seguridad"""
    try:
        result = safety_checker.check_input_safety(text)
        return result.get('is_safe', False)
    except Exception:
        return False
