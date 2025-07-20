import google.generativeai as genai
from .embedding_service import EmbeddingService
from .document_processor import DocumentProcessor
import logging
from ..config.settings import Config

logger = logging.getLogger(__name__)

class GeminiService:
    """Servicio para generar respuestas usando Gemini AI con RAG"""
    
    def __init__(self):
        # Configurar Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Inicializar servicios RAG
        self.embedding_service = EmbeddingService()
        self.document_processor = DocumentProcessor()
        
        # Inicializar documentos si es la primera vez
        self._initialize_documents()
    
    def _initialize_documents(self):
        """Inicializa los documentos en el vectorstore si están vacíos"""
        try:
            stats = self.embedding_service.get_vectorstore_stats()
            if stats.get('total_documents', 0) == 0:
                logger.info("Vectorstore vacío. Cargando documentos...")
                self._load_documents()
        except Exception as e:
            logger.error(f"Error inicializando documentos: {e}")
    
    def _load_documents(self):
        """Carga todos los documentos al vectorstore"""
        try:
            documents = self.document_processor.load_all_documents()
            if documents:
                success = self.embedding_service.add_documents(documents)
                if success:
                    logger.info(f"Documentos cargados exitosamente en RAG")
                else:
                    logger.error("Error cargando documentos en RAG")
            else:
                logger.warning("No se encontraron documentos para cargar")
        except Exception as e:
            logger.error(f"Error en _load_documents: {e}")
    
    def generate_response(self, message, user_context=None):
        """Genera respuesta usando RAG + Gemini"""
        try:
            # Buscar contexto relevante con RAG
            relevant_context = self.embedding_service.search_similar(message)
            
            # Construir prompt enriquecido
            enhanced_prompt = self._build_rag_prompt(message, relevant_context, user_context)
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(enhanced_prompt)
            
            return {
                'response': response.text,
                'sources_used': len(relevant_context),
                'context_found': bool(relevant_context)
            }
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return {
                'response': "Lo siento, hubo un error procesando tu consulta. Por favor intenta de nuevo.",
                'sources_used': 0,
                'context_found': False,
                'error': str(e)
            }
    
    def _build_rag_prompt(self, message, relevant_context, user_context=None):
        """Construye el prompt enriquecido con contexto RAG"""
        
        # Contexto base del sistema
        system_context = self._get_system_context()
        
        # Contexto de documentos (RAG)
        documents_context = ""
        if relevant_context:
            documents_context = "\\n\\nINFORMACIÓN RELEVANTE DE MIS DOCUMENTOS:\\n"
            for i, doc in enumerate(relevant_context, 1):
                documents_context += f"\\n[Fuente {i}]: {doc['content'][:500]}..."
                if doc.get('metadata', {}).get('filename'):
                    documents_context += f" (de: {doc['metadata']['filename']})"
        
        # Contexto de usuario si está disponible
        user_info = ""
        if user_context:
            user_info = f"\\n\\nCONTEXTO DEL USUARIO: {user_context}"
        
        # Prompt final
        prompt = f"""{system_context}
        
{documents_context}
{user_info}

CONSULTA DEL USUARIO: {message}

INSTRUCCIONES:
- Responde de manera profesional y amigable
- Usa SOLO la información de mis documentos cuando sea relevante
- Si no tienes información específica, sé honesto al respecto
- Mantén un tono conversacional pero profesional
- Si mencionas información de mis documentos, puedes hacer referencia general a ellos
- Adapta la respuesta al contexto de la consulta

RESPUESTA:"""
        
        return prompt
    
    def _get_system_context(self):
        """Retorna el contexto base del sistema"""
        return """Eres un asistente AI especializado en ayudar con consultas sobre mi perfil profesional y portfolio. 
        
Tu personalidad:
- Profesional pero amigable
- Conocedor de mi experiencia y habilidades
- Capaz de explicar proyectos técnicos de manera clara
- Entusiasta sobre tecnología y desarrollo

Tipos de consultas que puedes manejar:
- Información sobre mi experiencia profesional
- Detalles de proyectos desarrollados
- Habilidades técnicas y tecnologías
- Formación académica y certificaciones
- Información de contacto
- Disponibilidad para oportunidades laborales"""
    
    def reload_documents(self):
        """Recarga todos los documentos (útil para actualizaciones)"""
        try:
            logger.info("Recargando documentos...")
            self._load_documents()
            return {"success": True, "message": "Documentos recargados exitosamente"}
        except Exception as e:
            logger.error(f"Error recargando documentos: {e}")
            return {"success": False, "error": str(e)}
    
    def get_system_status(self):
        """Retorna el estado del sistema RAG"""
        try:
            vectorstore_stats = self.embedding_service.get_vectorstore_stats()
            documents_info = self.document_processor.get_documents_info()
            
            return {
                'vectorstore': vectorstore_stats,
                'documents': documents_info,
                'model': Config.GEMINI_MODEL,
                'embedding_model': Config.EMBEDDING_MODEL
            }
        except Exception as e:
            logger.error(f"Error obteniendo estado: {e}")
            return {"error": str(e)}