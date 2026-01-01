from google import genai
import os
import logging
from app.config.settings import Config

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY') or Config.GOOGLE_API_KEY
        if not api_key:
            logger.error("❌ GOOGLE_API_KEY no configurada")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            self.model = Config.GEMINI_MODEL
            logger.info(f"✅ GeminiService inicializado con {self.model}")

    async def generate(self, message: str, context: str) -> str:
        """Genera respuesta con contexto"""
        if not self.client:
            return "Error: API key no configurada"
            
        prompt = f"""
        Eres Heily, desarrolladora backend especializada en IA.
        Responde EN PRIMERA PERSONA.

        CONTEXTO:
        {context}

        PREGUNTA: {message}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Error en GeminiService: {str(e)}")
            return f"Error: {str(e)}"

gemini_service = GeminiService()

