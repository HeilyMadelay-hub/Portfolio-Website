import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class SectionType(Enum):
    """Tipos de sección del portfolio"""
    EXPERIENCIA = "experiencia"
    TECNOLOGIAS = "tecnologias"
    PROYECTOS = "proyectos"
    EDUCACION = "educacion"
    CONTACTO = "contacto"
    DISPONIBILIDAD = "disponibilidad"
    GENERAL = "general"

@dataclass
class SectionValidationRule:
    """Regla de validación para una sección"""
    section: SectionType
    required_keywords: List[str]
    forbidden_keywords: List[str]
    question_templates: List[str]
    guidance_message: str
    priority: int = 1

class SectionValidator:
    """
    Validador de secciones según diagrama híbrido
    SECTION_VALID -> SECTION_CHECK -> ENFORCE -> GUIDANCE
    """
    
    def __init__(self):
        self.validation_rules: Dict[SectionType, SectionValidationRule] = {}
        self.section_keywords: Dict[str, List[SectionType]] = {}
        
        # Inicializar reglas de validación
        self._load_validation_rules()
        self._build_keyword_index()
        
        logger.info(f"SectionValidator inicializado con {len(self.validation_rules)} secciones")
    
    def validate_section(self, message: str, intended_section: Optional[str] = None) -> Dict[str, any]:
        """
        Valida si el mensaje es apropiado para la sección
        
        Args:
            message: Mensaje del usuario
            intended_section: Sección intentada (si se especifica)
        
        Returns:
            Dict con is_valid, detected_section, guidance, enforcement_action
        """
        try:
            message_clean = message.lower().strip()
            
            # Detectar sección automáticamente
            detected_sections = self._detect_sections(message_clean)
            
            if intended_section:
                # Validar sección específica
                return self._validate_specific_section(message_clean, intended_section, detected_sections)
            else:
                # Validación general
                return self._validate_general_message(message_clean, detected_sections)
                
        except Exception as e:
            logger.error(f"Error validando sección: {e}")
            return {
                'is_valid': True,  # Fail-open en caso de error
                'detected_section': SectionType.GENERAL.value,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _load_validation_rules(self):
        """Carga reglas de validación para cada sección"""
        rules = [
            SectionValidationRule(
                section=SectionType.EXPERIENCIA,
                required_keywords=["experiencia", "trabajo", "laboral", "años", "profesional", "carrera"],
                forbidden_keywords=["contacto", "email", "telefono", "precio", "costo"],
                question_templates=[
                    "¿Qué experiencia profesional tienes?",
                    "¿Cuántos años de experiencia tienes?",
                    "¿En qué empresas has trabajado?",
                    "¿Cuál es tu trayectoria laboral?"
                ],
                guidance_message="Para preguntas sobre experiencia laboral, puedes preguntar sobre: años de experiencia, empresas donde he trabajado, roles desempeñados, o logros profesionales.",
                priority=1
            ),
            
            SectionValidationRule(
                section=SectionType.TECNOLOGIAS,
                required_keywords=["tecnologías", "lenguajes", "frameworks", "herramientas", "stack", "programación"],
                forbidden_keywords=["salario", "contacto", "personal"],
                question_templates=[
                    "¿Qué tecnologías manejas?",
                    "¿Cuál es tu stack tecnológico?",
                    "¿Qué lenguajes de programación conoces?",
                    "¿Qué frameworks usas?"
                ],
                guidance_message="Para preguntas sobre tecnologías, puedes preguntar sobre: lenguajes de programación, frameworks, herramientas de desarrollo, bases de datos, o mi stack tecnológico.",
                priority=1
            ),
            
            SectionValidationRule(
                section=SectionType.PROYECTOS,
                required_keywords=["proyectos", "portfolio", "desarrollado", "construido", "creado", "trabajo"],
                forbidden_keywords=["personal", "familia", "privado"],
                question_templates=[
                    "¿Qué proyectos has desarrollado?",
                    "¿Puedes mostrarme tu portfolio?",
                    "¿Qué has construido recientemente?",
                    "¿Cuáles son tus mejores proyectos?"
                ],
                guidance_message="Para preguntas sobre proyectos, puedes preguntar sobre: proyectos desarrollados, tecnologías utilizadas, desafíos resueltos, o resultados obtenidos.",
                priority=1
            ),
            
            SectionValidationRule(
                section=SectionType.EDUCACION,
                required_keywords=["educación", "estudios", "formación", "título", "certificaciones", "cursos"],
                forbidden_keywords=["trabajo", "salario", "empresa"],
                question_templates=[
                    "¿Qué estudiaste?",
                    "¿Cuál es tu formación académica?",
                    "¿Tienes certificaciones?",
                    "¿Dónde estudiaste?"
                ],
                guidance_message="Para preguntas sobre educación, puedes preguntar sobre: formación académica, certificaciones, cursos completados, o estudios en progreso.",
                priority=2
            ),
            
            SectionValidationRule(
                section=SectionType.CONTACTO,
                required_keywords=["contacto", "email", "linkedin", "telefono", "ubicación", "contactar"],
                forbidden_keywords=["tecnologías", "experiencia", "proyectos"],
                question_templates=[
                    "¿Cómo puedo contactarte?",
                    "¿Cuál es tu email?",
                    "¿Tienes LinkedIn?",
                    "¿Dónde te ubico?"
                ],
                guidance_message="Para información de contacto, puedes preguntar sobre: email, LinkedIn, redes sociales profesionales, o formas de comunicación.",
                priority=1
            ),
            
            SectionValidationRule(
                section=SectionType.DISPONIBILIDAD,
                required_keywords=["disponible", "trabajo", "empleo", "contratar", "oportunidades", "busco"],
                forbidden_keywords=["pasado", "anterior", "estudios"],
                question_templates=[
                    "¿Estás disponible para trabajar?",
                    "¿Buscas empleo?",
                    "¿Te puedo contratar?",
                    "¿Estás buscando oportunidades?"
                ],
                guidance_message="Para preguntas sobre disponibilidad, puedes preguntar sobre: disponibilidad laboral, tipo de trabajo que busco, modalidad preferida, o ubicación.",
                priority=1
            )
        ]
        
        # Cargar reglas al diccionario
        for rule in rules:
            self.validation_rules[rule.section] = rule
    
    def _build_keyword_index(self):
        """Construye índice de keywords por sección"""
        self.section_keywords = {}
        
        for section, rule in self.validation_rules.items():
            for keyword in rule.required_keywords:
                if keyword not in self.section_keywords:
                    self.section_keywords[keyword] = []
                self.section_keywords[keyword].append(section)
    
    def _detect_sections(self, message: str) -> List[Tuple[SectionType, float]]:
        """Detecta secciones relevantes en el mensaje"""
        section_scores = {}
        words = message.split()
        
        # Puntuar por keywords
        for word in words:
            if word in self.section_keywords:
                for section in self.section_keywords[word]:
                    if section not in section_scores:
                        section_scores[section] = 0
                    section_scores[section] += 1
        
        # Normalizar scores
        if section_scores:
            max_score = max(section_scores.values())
            normalized_scores = [
                (section, score / max_score) 
                for section, score in section_scores.items()
            ]
        else:
            normalized_scores = [(SectionType.GENERAL, 1.0)]
        
        # Ordenar por score descendente
        return sorted(normalized_scores, key=lambda x: x[1], reverse=True)
    
    def _validate_specific_section(self, message: str, intended_section: str, detected_sections: List) -> Dict[str, any]:
        """Valida mensaje para una sección específica"""
        try:
            section_enum = SectionType(intended_section.lower())
        except ValueError:
            return {
                'is_valid': False,
                'error': f"Sección no válida: {intended_section}",
                'detected_section': SectionType.GENERAL.value,
                'enforcement_action': 'redirect',
                'guidance': "Las secciones válidas son: experiencia, tecnologias, proyectos, educacion, contacto, disponibilidad"
            }
        
        if section_enum not in self.validation_rules:
            return {
                'is_valid': False,
                'error': f"Reglas no encontradas para sección: {intended_section}",
                'detected_section': SectionType.GENERAL.value,
                'enforcement_action': 'redirect'
            }
        
        rule = self.validation_rules[section_enum]
        
        # Verificar keywords requeridas
        required_found = any(keyword in message for keyword in rule.required_keywords)
        
        # Verificar keywords prohibidas
        forbidden_found = any(keyword in message for keyword in rule.forbidden_keywords)
        
        # Determinar si la sección detectada coincide
        detected_section = detected_sections[0][0] if detected_sections else SectionType.GENERAL
        section_matches = detected_section == section_enum
        
        if required_found and not forbidden_found and section_matches:
            return {
                'is_valid': True,
                'detected_section': section_enum.value,
                'confidence': detected_sections[0][1] if detected_sections else 0.5,
                'enforcement_action': 'proceed'
            }
        else:
            return {
                'is_valid': False,
                'detected_section': detected_section.value,
                'intended_section': intended_section,
                'enforcement_action': 'guide',
                'guidance': rule.guidance_message,
                'question_templates': rule.question_templates,
                'issues': {
                    'missing_required_keywords': not required_found,
                    'forbidden_keywords_present': forbidden_found,
                    'section_mismatch': not section_matches
                }
            }
    
    def _validate_general_message(self, message: str, detected_sections: List) -> Dict[str, any]:
        """Validación general sin sección específica"""
        if not detected_sections:
            return {
                'is_valid': True,
                'detected_section': SectionType.GENERAL.value,
                'confidence': 1.0,
                'enforcement_action': 'proceed'
            }
        
        # Usar la sección detectada con mayor confianza
        primary_section, confidence = detected_sections[0]
        
        # Verificar si hay conflicto entre secciones detectadas
        conflicting_sections = [s for s, c in detected_sections[1:] if c > 0.3]
        
        if conflicting_sections:
            return {
                'is_valid': False,
                'detected_section': primary_section.value,
                'confidence': confidence,
                'enforcement_action': 'clarify',
                'guidance': f"Tu pregunta podría ser sobre {primary_section.value}, pero también detecté elementos de {[s.value for s in conflicting_sections]}. ¿Podrías ser más específico?",
                'conflicting_sections': [s.value for s in conflicting_sections]
            }
        
        return {
            'is_valid': True,
            'detected_section': primary_section.value,
            'confidence': confidence,
            'enforcement_action': 'proceed'
        }
    
    def get_section_guidance(self, section: str) -> Dict[str, any]:
        """Obtiene guía para una sección específica"""
        try:
            section_enum = SectionType(section.lower())
            if section_enum in self.validation_rules:
                rule = self.validation_rules[section_enum]
                return {
                    'section': section,
                    'guidance': rule.guidance_message,
                    'question_templates': rule.question_templates,
                    'keywords': rule.required_keywords
                }
        except ValueError:
            pass
        
        return {
            'section': section,
            'error': 'Sección no encontrada',
            'available_sections': [s.value for s in SectionType]
        }
    
    def get_all_sections(self) -> List[Dict[str, any]]:
        """Obtiene información de todas las secciones"""
        sections = []
        for section_type, rule in self.validation_rules.items():
            sections.append({
                'section': section_type.value,
                'guidance': rule.guidance_message,
                'question_templates': rule.question_templates[:2],  # Solo primeros 2
                'keywords_count': len(rule.required_keywords),
                'priority': rule.priority
            })
        
        return sorted(sections, key=lambda x: x['priority'])
    
    def get_stats(self) -> Dict[str, any]:
        """Estadísticas del validador de secciones"""
        return {
            'total_sections': len(self.validation_rules),
            'total_keywords': len(self.section_keywords),
            'sections': [s.value for s in self.validation_rules.keys()],
            'keywords_per_section': {
                s.value: len(rule.required_keywords) 
                for s, rule in self.validation_rules.items()
            }
        }

# Instancia global del validador de secciones
section_validator = SectionValidator()

def validate_message_section(message: str, intended_section: str = None) -> Dict[str, any]:
    """Función helper para validar secciones"""
    return section_validator.validate_section(message, intended_section)

def get_section_guidance_message(section: str) -> str:
    """Obtiene mensaje de guía para una sección"""
    result = section_validator.get_section_guidance(section)
    return result.get('guidance', 'Sección no encontrada')

def detect_message_section(message: str) -> str:
    """Detecta la sección principal de un mensaje"""
    try:
        result = section_validator.validate_section(message)
        return result.get('detected_section', 'general')
    except Exception:
        return 'general'
