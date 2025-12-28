import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

@dataclass
class FAQItem:
    """Elemento de FAQ"""
    id: str
    question_patterns: List[str]
    response: str
    keywords: List[str]
    category: str
    priority: int = 1  # 1 = alta, 2 = media, 3 = baja
    language: str = "es"

class FAQClassifier:
    """
    Clasificador de FAQ según diagrama híbrido
    FAQ_CLASSIFIER -> FAQ_RESP (bypass RAG para consultas comunes)
    """
    
    def __init__(self):
        self.faqs: Dict[str, FAQItem] = {}
        self.keyword_index: Dict[str, List[str]] = {}
        
        # Inicializar FAQs predefinidas
        self._load_default_faqs()
        self._build_keyword_index()
        
        logger.info(f"FAQClassifier inicializado con {len(self.faqs)} FAQs")
    
    def classify_message(self, message: str) -> Dict[str, any]:
        """
        Clasifica mensaje para determinar si es FAQ
        
        Args:
            message: Mensaje del usuario
        
        Returns:
            Dict con is_faq, confidence, faq_id, response
        """
        try:
            message_clean = self._normalize_message(message)
            
            # Búsqueda por patrones exactos (alta confianza)
            pattern_match = self._search_by_patterns(message_clean)
            if pattern_match:
                return {
                    'is_faq': True,
                    'confidence': pattern_match['confidence'],
                    'faq_id': pattern_match['faq_id'],
                    'response': pattern_match['response'],
                    'method': 'pattern_match',
                    'category': pattern_match['category']
                }
            
            # Búsqueda por keywords (confianza media)
            keyword_match = self._search_by_keywords(message_clean)
            if keyword_match and keyword_match['confidence'] > 0.7:
                return {
                    'is_faq': True,
                    'confidence': keyword_match['confidence'],
                    'faq_id': keyword_match['faq_id'],
                    'response': keyword_match['response'],
                    'method': 'keyword_match',
                    'category': keyword_match['category']
                }
            
            # Búsqueda por similitud (confianza baja-media)
            similarity_match = self._search_by_similarity(message_clean)
            if similarity_match and similarity_match['confidence'] > 0.8:
                return {
                    'is_faq': True,
                    'confidence': similarity_match['confidence'],
                    'faq_id': similarity_match['faq_id'],
                    'response': similarity_match['response'],
                    'method': 'similarity_match',
                    'category': similarity_match['category']
                }
            
            # No es FAQ - proceder con RAG
            return {
                'is_faq': False,
                'confidence': 0.0,
                'reason': 'No se encontró coincidencia en FAQs'
            }
            
        except Exception as e:
            logger.error(f"Error clasificando mensaje: {e}")
            return {
                'is_faq': False,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _load_default_faqs(self):
        """Carga FAQs predefinidas del portfolio"""
        default_faqs = [
            # EXPERIENCIA
            FAQItem(
                id="exp_general",
                question_patterns=[
                    r"qu[eé] experiencia tienes?",
                    r"cu[aá]ntos a[ñn]os de experiencia",
                    r"cu[eé]ntame (de|sobre) tu experiencia",
                    r"experiencia laboral",
                    r"trabajo previo"
                ],
                response="Tengo experiencia como desarrollador full-stack trabajando con tecnologías modernas como React, Python, Node.js y bases de datos. He desarrollado aplicaciones web completas, APIs REST y sistemas de gestión de datos.",
                keywords=["experiencia", "años", "trabajo", "laboral", "profesional"],
                category="experiencia",
                priority=1
            ),
            
            # TECNOLOGÍAS
            FAQItem(
                id="tech_stack",
                question_patterns=[
                    r"qu[eé] tecnolog[ií]as (usas|manejas|conoces)",
                    r"cu[aá]l es tu stack tecnol[oó]gico",
                    r"qu[eé] lenguajes de programaci[oó]n",
                    r"herramientas que (usas|dominas)",
                    r"frameworks que conoces"
                ],
                response="Mi stack tecnológico incluye: Frontend (React, JavaScript, HTML, CSS), Backend (Python, Flask, Node.js), Bases de datos (PostgreSQL, MongoDB), Cloud (Google Cloud, AWS), IA (Google Gemini, RAG, ChromaDB) y herramientas de desarrollo modernas.",
                keywords=["tecnologías", "stack", "lenguajes", "frameworks", "herramientas", "programación"],
                category="tecnologias",
                priority=1
            ),
            
            # PROYECTOS
            FAQItem(
                id="projects_general",
                question_patterns=[
                    r"qu[eé] proyectos has (desarrollado|hecho|creado)",
                    r"muéstrame tu trabajo",
                    r"portfolio de proyectos",
                    r"ejemplos de tu trabajo",
                    r"qu[eé] has construido"
                ],
                response="He desarrollado varios proyectos incluyendo: chatbots con IA y RAG, aplicaciones web full-stack, sistemas de gestión de datos, APIs REST, y integraciones con servicios de cloud. Cada proyecto demuestra diferentes aspectos de mi experiencia técnica.",
                keywords=["proyectos", "portfolio", "trabajo", "desarrollado", "construido", "ejemplos"],
                category="proyectos",
                priority=1
            ),
            
            # CONTACTO
            FAQItem(
                id="contact_info",
                question_patterns=[
                    r"c[oó]mo puedo contactarte",
                    r"cu[aá]l es tu (email|correo)",
                    r"informaci[oó]n de contacto",
                    r"d[oó]nde te encuentro",
                    r"c[oó]mo te ubico"
                ],
                response="Puedes contactarme a través de mi email o LinkedIn. Estoy disponible para discutir oportunidades de trabajo, colaboraciones o preguntas técnicas sobre mis proyectos.",
                keywords=["contacto", "email", "correo", "linkedin", "ubicar", "encontrar"],
                category="contacto",
                priority=1
            ),
            
            # DISPONIBILIDAD
            FAQItem(
                id="availability",
                question_patterns=[
                    r"est[aá]s disponible para trabajar",
                    r"buscas trabajo",
                    r"est[aá]s buscando empleo",
                    r"disponibilidad laboral",
                    r"puedes trabajar en"
                ],
                response="Sí, estoy disponible para nuevas oportunidades laborales. Busco posiciones como desarrollador full-stack donde pueda aplicar mis habilidades en desarrollo web, IA y tecnologías modernas.",
                keywords=["disponible", "trabajo", "empleo", "oportunidades", "laborales", "busco"],
                category="disponibilidad",
                priority=1
            ),
            
            # EDUCACIÓN
            FAQItem(
                id="education",
                question_patterns=[
                    r"qu[eé] estudiaste",
                    r"cu[aá]l es tu formaci[oó]n",
                    r"tienes t[ií]tulo",
                    r"educaci[oó]n acad[eé]mica",
                    r"certificaciones"
                ],
                response="Mi formación incluye estudios en desarrollo de software y tecnologías de la información. Además, mantengo actualizadas mis habilidades a través de cursos online, certificaciones y práctica constante con nuevas tecnologías.",
                keywords=["educación", "estudios", "formación", "título", "certificaciones", "académica"],
                category="educacion",
                priority=2
            ),
            
            # SALUDO/INTRODUCCIÓN
            FAQItem(
                id="greeting",
                question_patterns=[
                    r"^(hola|hello|hi|hey)$",
                    r"qu[eé] tal",
                    r"c[oó]mo est[aá]s",
                    r"buenos d[ií]as",
                    r"buenas tardes"
                ],
                response="¡Hola! Soy un asistente IA que puede ayudarte con preguntas sobre mi perfil profesional, experiencia, proyectos y habilidades técnicas. ¿En qué puedo ayudarte?",
                keywords=["hola", "saludo", "hey", "hi", "hello"],
                category="saludo",
                priority=3
            ),
            
            # AYUDA
            FAQItem(
                id="help",
                question_patterns=[
                    r"qu[eé] puedes hacer",
                    r"c[oó]mo puedes ayudarme",
                    r"qu[eé] preguntas puedo hacer",
                    r"ayuda",
                    r"help"
                ],
                response="Puedo ayudarte con información sobre: experiencia profesional, tecnologías que manejo, proyectos desarrollados, educación y formación, información de contacto, y disponibilidad laboral. ¡Pregunta lo que necesites saber!",
                keywords=["ayuda", "help", "puedes", "preguntas", "información"],
                category="ayuda",
                priority=3
            )
        ]
        
        # Cargar FAQs al diccionario
        for faq in default_faqs:
            self.faqs[faq.id] = faq
    
    def _build_keyword_index(self):
        """Construye índice de keywords para búsqueda rápida"""
        self.keyword_index = {}
        
        for faq_id, faq in self.faqs.items():
            for keyword in faq.keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(faq_id)
    
    def _normalize_message(self, message: str) -> str:
        """Normaliza mensaje para búsqueda"""
        # Convertir a minúsculas
        normalized = message.lower().strip()
        
        # Remover caracteres especiales excepto espacios y acentos
        normalized = re.sub(r'[^\w\s\?¿¡!]', ' ', normalized)
        
        # Normalizar espacios múltiples
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized
    
    def _search_by_patterns(self, message: str) -> Optional[Dict]:
        """Búsqueda por patrones regex (alta precisión)"""
        best_match = None
        best_confidence = 0.0
        
        for faq_id, faq in self.faqs.items():
            for pattern in faq.question_patterns:
                try:
                    if re.search(pattern, message, re.IGNORECASE):
                        # Calcular confianza basada en la longitud del match
                        match = re.search(pattern, message, re.IGNORECASE)
                        confidence = len(match.group()) / len(message)
                        confidence = min(confidence * 1.2, 1.0)  # Boost para matches exactos
                        
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_match = {
                                'faq_id': faq_id,
                                'response': faq.response,
                                'confidence': confidence,
                                'category': faq.category
                            }
                except re.error:
                    logger.warning(f"Patrón regex inválido en FAQ {faq_id}: {pattern}")
        
        return best_match if best_confidence > 0.6 else None
    
    def _search_by_keywords(self, message: str) -> Optional[Dict]:
        """Búsqueda por keywords (precisión media)"""
        message_words = set(message.split())
        faq_scores = {}
        
        # Puntuar FAQs basado en keywords encontradas
        for word in message_words:
            if word in self.keyword_index:
                for faq_id in self.keyword_index[word]:
                    if faq_id not in faq_scores:
                        faq_scores[faq_id] = 0
                    faq_scores[faq_id] += 1
        
        if not faq_scores:
            return None
        
        # Encontrar mejor match
        best_faq_id = max(faq_scores, key=faq_scores.get)
        faq = self.faqs[best_faq_id]
        
        # Calcular confianza
        matches = faq_scores[best_faq_id]
        total_keywords = len(faq.keywords)
        confidence = (matches / total_keywords) * 0.8  # Max 0.8 para keyword matches
        
        return {
            'faq_id': best_faq_id,
            'response': faq.response,
            'confidence': confidence,
            'category': faq.category
        } if confidence > 0.4 else None
    
    def _search_by_similarity(self, message: str) -> Optional[Dict]:
        """Búsqueda por similitud de texto (baja precisión, alta cobertura)"""
        best_match = None
        best_similarity = 0.0
        
        for faq_id, faq in self.faqs.items():
            for pattern in faq.question_patterns:
                # Remover regex especiales para comparación de similitud
                clean_pattern = re.sub(r'[^\w\s]', '', pattern).lower()
                
                similarity = SequenceMatcher(None, message, clean_pattern).ratio()
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = {
                        'faq_id': faq_id,
                        'response': faq.response,
                        'confidence': similarity * 0.9,  # Reducir confianza para matches de similitud
                        'category': faq.category
                    }
        
        return best_match if best_similarity > 0.7 else None
    
    def add_faq(self, faq: FAQItem) -> bool:
        """Agrega nueva FAQ dinámicamente"""
        try:
            self.faqs[faq.id] = faq
            
            # Actualizar índice de keywords
            for keyword in faq.keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(faq.id)
            
            logger.info(f"FAQ agregada: {faq.id}")
            return True
        except Exception as e:
            logger.error(f"Error agregando FAQ {faq.id}: {e}")
            return False
    
    def get_faq_by_category(self, category: str) -> List[FAQItem]:
        """Obtiene todas las FAQs de una categoría"""
        return [faq for faq in self.faqs.values() if faq.category == category]
    
    def get_stats(self) -> Dict[str, any]:
        """Estadísticas del clasificador FAQ"""
        categories = {}
        priorities = {}
        
        for faq in self.faqs.values():
            categories[faq.category] = categories.get(faq.category, 0) + 1
            priorities[faq.priority] = priorities.get(faq.priority, 0) + 1
        
        return {
            'total_faqs': len(self.faqs),
            'categories': categories,
            'priorities': priorities,
            'keywords_indexed': len(self.keyword_index)
        }

# Instancia global del clasificador FAQ
faq_classifier = FAQClassifier()

def classify_user_message(message: str) -> Dict[str, any]:
    """Función helper para clasificar mensajes"""
    return faq_classifier.classify_message(message)

def is_faq_message(message: str, min_confidence: float = 0.7) -> bool:
    """Verificación rápida si es FAQ"""
    try:
        result = faq_classifier.classify_message(message)
        return result.get('is_faq', False) and result.get('confidence', 0) >= min_confidence
    except Exception:
        return False
