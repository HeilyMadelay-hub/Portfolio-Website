import logging
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class Language(Enum):
    """Idiomas soportados"""
    SPANISH = "es"
    ENGLISH = "en"

@dataclass
class Translation:
    """Traducción de un texto"""
    key: str
    es: str
    en: str
    category: str = "general"

class I18nService:
    """
    Servicio de internacionalización según diagrama híbrido
    RESP_STRUCT -> I18N -> RESP_FINAL
    """
    
    def __init__(self):
        self.translations: Dict[str, Translation] = {}
        self.default_language = Language.SPANISH
        
        # Cargar traducciones predefinidas
        self._load_translations()
        
        logger.info(f"I18nService inicializado con {len(self.translations)} traducciones")
    
    def translate_response(self, response_data: Dict[str, Any], target_language: str = "es") -> Dict[str, Any]:
        """
        Traduce respuesta completa según el idioma objetivo
        
        Args:
            response_data: Datos de respuesta a traducir
            target_language: Idioma objetivo (es/en)
        
        Returns:
            Dict con respuesta traducida
        """
        try:
            lang = Language(target_language.lower())
        except ValueError:
            lang = self.default_language
            logger.warning(f"Idioma no soportado: {target_language}, usando {lang.value}")
        
        try:
            translated_data = response_data.copy()
            
            # Traducir respuesta principal
            if 'response' in translated_data:
                translated_data['response'] = self._translate_text(
                    translated_data['response'], lang
                )
            
            # Traducir metadata
            if 'metadata' in translated_data:
                translated_data['metadata'] = self._translate_metadata(
                    translated_data['metadata'], lang
                )
            
            # Traducir mensajes de error
            if 'error' in translated_data:
                translated_data['error'] = self._translate_error(
                    translated_data['error'], lang
                )
            
            # Traducir mensajes de guía
            if 'guidance' in translated_data:
                translated_data['guidance'] = self._translate_guidance(
                    translated_data['guidance'], lang
                )
            
            # Agregar información de idioma
            translated_data['language'] = lang.value
            translated_data['i18n_applied'] = True
            
            return translated_data
            
        except Exception as e:
            logger.error(f"Error traduciendo respuesta: {e}")
            # En caso de error, retornar respuesta original con marcador de error
            response_data['language'] = self.default_language.value
            response_data['i18n_error'] = str(e)
            return response_data
    
    def detect_language(self, text: str) -> Language:
        """
        Detecta el idioma de un texto
        
        Args:
            text: Texto a analizar
        
        Returns:
            Language detectado
        """
        try:
            text_lower = text.lower()
            
            # Palabras indicadoras de español
            spanish_indicators = [
                'qué', 'cuál', 'cómo', 'dónde', 'cuándo', 'por qué',
                'experiencia', 'trabajo', 'habilidades', 'proyectos',
                'tecnologías', 'contacto', 'disponible', 'ñ'
            ]
            
            # Palabras indicadoras de inglés
            english_indicators = [
                'what', 'which', 'how', 'where', 'when', 'why',
                'experience', 'work', 'skills', 'projects',
                'technologies', 'contact', 'available'
            ]
            
            spanish_score = sum(1 for word in spanish_indicators if word in text_lower)
            english_score = sum(1 for word in english_indicators if word in text_lower)
            
            # Si hay empate o no hay indicadores claros, usar español por defecto
            if spanish_score >= english_score:
                return Language.SPANISH
            else:
                return Language.ENGLISH
                
        except Exception as e:
            logger.error(f"Error detectando idioma: {e}")
            return self.default_language
    
    def _load_translations(self):
        """Carga traducciones predefinidas"""
        translations = [
            # Mensajes del sistema
            Translation(
                key="system_error",
                es="Lo siento, hubo un error procesando tu consulta. Por favor intenta de nuevo.",
                en="Sorry, there was an error processing your request. Please try again.",
                category="system"
            ),
            
            Translation(
                key="rate_limit_exceeded",
                es="Has excedido el límite de consultas. Por favor espera un momento antes de intentar de nuevo.",
                en="You have exceeded the query limit. Please wait a moment before trying again.",
                category="system"
            ),
            
            Translation(
                key="input_too_long",
                es="Tu mensaje es muy largo. Por favor acórtalo a menos de 500 caracteres.",
                en="Your message is too long. Please shorten it to less than 500 characters.",
                category="validation"
            ),
            
            Translation(
                key="inappropriate_content",
                es="No puedo procesar ese tipo de contenido. Por favor haz una pregunta relacionada con mi perfil profesional.",
                en="I cannot process that type of content. Please ask a question related to my professional profile.",
                category="safety"
            ),
            
            # Respuestas de emergencia
            Translation(
                key="emergency_mode_active",
                es="Actualmente tengo problemas técnicos. Mi capacidad de respuesta está limitada temporalmente.",
                en="I'm currently experiencing technical issues. My response capability is temporarily limited.",
                category="emergency"
            ),
            
            Translation(
                key="services_unavailable",
                es="Algunos servicios no están disponibles en este momento. Intenta de nuevo más tarde.",
                en="Some services are currently unavailable. Please try again later.",
                category="emergency"
            ),
            
            # Mensajes de guía
            Translation(
                key="section_guidance_experience",
                es="Para preguntas sobre experiencia, puedes preguntar sobre: años de experiencia, empresas donde he trabajado, roles desempeñados.",
                en="For experience questions, you can ask about: years of experience, companies I've worked for, roles performed.",
                category="guidance"
            ),
            
            Translation(
                key="section_guidance_technologies",
                es="Para preguntas sobre tecnologías, puedes preguntar sobre: lenguajes de programación, frameworks, herramientas de desarrollo.",
                en="For technology questions, you can ask about: programming languages, frameworks, development tools.",
                category="guidance"
            ),
            
            Translation(
                key="section_guidance_projects",
                es="Para preguntas sobre proyectos, puedes preguntar sobre: proyectos desarrollados, tecnologías utilizadas, desafíos resueltos.",
                en="For project questions, you can ask about: developed projects, technologies used, challenges solved.",
                category="guidance"
            ),
            
            # Metadata
            Translation(
                key="sources_used",
                es="fuentes utilizadas",
                en="sources used",
                category="metadata"
            ),
            
            Translation(
                key="context_found",
                es="contexto encontrado",
                en="context found",
                category="metadata"
            ),
            
            Translation(
                key="from_cache",
                es="desde caché",
                en="from cache",
                category="metadata"
            ),
            
            # FAQ responses  
            Translation(
                key="greeting_response",
                es="¡Hola! Soy un asistente IA que puede ayudarte con preguntas sobre mi perfil profesional. ¿En qué puedo ayudarte?",
                en="Hello! I'm an AI assistant that can help you with questions about my professional profile. How can I help you?",
                category="faq"
            ),
            
            Translation(
                key="help_response",
                es="Puedo ayudarte con información sobre: experiencia profesional, tecnologías, proyectos, educación e información de contacto.",
                en="I can help you with information about: professional experience, technologies, projects, education, and contact information.",
                category="faq"
            )
        ]
        
        # Cargar traducciones al diccionario
        for translation in translations:
            self.translations[translation.key] = translation
    
    def _translate_text(self, text: str, target_lang: Language) -> str:
        """Traduce texto usando las traducciones predefinidas o pasándolo como está"""
        # Buscar traducción exacta
        for key, translation in self.translations.items():
            if target_lang == Language.SPANISH and text == translation.en:
                return translation.es
            elif target_lang == Language.ENGLISH and text == translation.es:
                return translation.en
        
        # Si no hay traducción exacta, buscar por coincidencias parciales
        translated_text = text
        for key, translation in self.translations.items():
            if target_lang == Language.SPANISH:
                translated_text = translated_text.replace(translation.en, translation.es)
            elif target_lang == Language.ENGLISH:
                translated_text = translated_text.replace(translation.es, translation.en)
        
        return translated_text
    
    def _translate_metadata(self, metadata: Dict[str, Any], target_lang: Language) -> Dict[str, Any]:
        """Traduce campos de metadata"""
        translated_metadata = metadata.copy()
        
        # Traducir claves específicas de metadata
        translation_map = {
            'sources_used': self.get_translation('sources_used', target_lang),
            'context_found': self.get_translation('context_found', target_lang),
            'from_cache': self.get_translation('from_cache', target_lang)
        }
        
        for key, translated_value in translation_map.items():
            if key in translated_metadata:
                # Mantener el valor original pero agregar traducción si es texto
                if isinstance(translated_metadata[key], str):
                    translated_metadata[f"{key}_translated"] = translated_value
        
        return translated_metadata
    
    def _translate_error(self, error_message: str, target_lang: Language) -> str:
        """Traduce mensajes de error"""
        # Mapeo de errores comunes
        error_mappings = {
            "rate limit": "rate_limit_exceeded",
            "too long": "input_too_long", 
            "inappropriate": "inappropriate_content",
            "system error": "system_error"
        }
        
        error_lower = error_message.lower()
        for pattern, key in error_mappings.items():
            if pattern in error_lower:
                return self.get_translation(key, target_lang)
        
        # Si no hay mapeo específico, traducir texto directamente
        return self._translate_text(error_message, target_lang)
    
    def _translate_guidance(self, guidance_message: str, target_lang: Language) -> str:
        """Traduce mensajes de guía"""
        guidance_lower = guidance_message.lower()
        
        # Detectar tipo de guía por contenido
        if "experiencia" in guidance_lower or "experience" in guidance_lower:
            return self.get_translation("section_guidance_experience", target_lang)
        elif "tecnolog" in guidance_lower or "technolog" in guidance_lower:
            return self.get_translation("section_guidance_technologies", target_lang)
        elif "proyecto" in guidance_lower or "project" in guidance_lower:
            return self.get_translation("section_guidance_projects", target_lang)
        
        # Si no hay guía específica, traducir texto directamente
        return self._translate_text(guidance_message, target_lang)
    
    def get_translation(self, key: str, target_lang: Language) -> str:
        """Obtiene traducción específica por clave"""
        try:
            if key in self.translations:
                translation = self.translations[key]
                if target_lang == Language.SPANISH:
                    return translation.es
                elif target_lang == Language.ENGLISH:
                    return translation.en
            
            logger.warning(f"Traducción no encontrada para clave: {key}")
            return key  # Retornar clave como fallback
            
        except Exception as e:
            logger.error(f"Error obteniendo traducción {key}: {e}")
            return key
    
    def add_translation(self, translation: Translation) -> bool:
        """Agrega nueva traducción"""
        try:
            self.translations[translation.key] = translation
            logger.info(f"Traducción agregada: {translation.key}")
            return True
        except Exception as e:
            logger.error(f"Error agregando traducción {translation.key}: {e}")
            return False
    
    def get_supported_languages(self) -> List[str]:
        """Obtiene lista de idiomas soportados"""
        return [lang.value for lang in Language]
    
    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas del servicio de i18n"""
        categories = {}
        for translation in self.translations.values():
            categories[translation.category] = categories.get(translation.category, 0) + 1
        
        return {
            'total_translations': len(self.translations),
            'supported_languages': self.get_supported_languages(),
            'default_language': self.default_language.value,
            'categories': categories
        }

# Instancia global del servicio i18n
i18n_service = I18nService()

def translate_response(response_data: Dict[str, Any], target_language: str = "es") -> Dict[str, Any]:
    """Función helper para traducir respuestas"""
    return i18n_service.translate_response(response_data, target_language)

def detect_user_language(text: str) -> str:
    """Función helper para detectar idioma"""
    return i18n_service.detect_language(text).value

def get_localized_message(key: str, language: str = "es") -> str:
    """Función helper para obtener mensajes localizados"""
    try:
        lang = Language(language.lower())
        return i18n_service.get_translation(key, lang)
    except ValueError:
        return i18n_service.get_translation(key, Language.SPANISH)
