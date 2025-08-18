import google.generativeai as genai
import logging
from typing import List, Dict, Any
from ..interfaces import ILLMProvider, IEmbeddingProvider
from ..config.settings import Config

logger = logging.getLogger(__name__)

class GeminiLLMProvider(ILLMProvider):
    """Implementación de Gemini para LLM"""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self._available = self._check_availability()
    
    def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Genera respuesta usando Gemini"""
        try:
            if not self._available:
                return {
                    'success': False,
                    'response': 'Servicio LLM no disponible',
                    'error': 'Provider not available'
                }
            
            response = self.model.generate_content(prompt)
            
            return {
                'success': True,
                'response': response.text,
                'model': Config.GEMINI_MODEL,
                'provider': 'gemini'
            }
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return {
                'success': False,
                'response': 'Error procesando consulta',
                'error': str(e)
            }
    
    def is_available(self) -> bool:
        """Verifica disponibilidad del servicio"""
        return self._available
    
    def get_model_info(self) -> Dict[str, str]:
        """Información del modelo"""
        return {
            'provider': 'Google Gemini',
            'model': Config.GEMINI_MODEL,
            'version': '1.0',
            'type': 'generative'
        }
    
    def _check_availability(self) -> bool:
        """Verifica si Gemini está disponible"""
        try:
            # Test más simple para evitar problemas de autenticación
            return bool(Config.GOOGLE_API_KEY and len(Config.GOOGLE_API_KEY) > 20)
        except Exception as e:
            logger.warning(f"Gemini no disponible: {e}")
            return False


class GeminiEmbeddingProvider(IEmbeddingProvider):
    """Implementación de Gemini para embeddings"""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self._available = self._check_availability()  # ✅ CORREGIDO: Inicializar _available
    
    def generate_embedding(self, text: str) -> List[float]:
        """Genera embedding usando Gemini"""
        try:
            if not self._available:
                logger.warning("Embedding provider no disponible")
                return []
            
            result = genai.embed_content(
                model=Config.EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
            
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return []
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Genera embeddings de múltiples textos"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def is_available(self) -> bool:
        """Verifica disponibilidad"""
        return self._available
    
    def _check_availability(self) -> bool:
        """Verifica si el servicio de embeddings está disponible"""
        try:
            # Verificación simple sin hacer llamada real
            return bool(Config.GOOGLE_API_KEY and len(Config.GOOGLE_API_KEY) > 20)
        except Exception as e:
            logger.warning(f"Embeddings no disponibles: {e}")
            return False
