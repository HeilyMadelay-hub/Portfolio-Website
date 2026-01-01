import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("❌ GOOGLE_API_KEY no configurada")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ GeminiService inicializado")

    async def generate(self, message: str, context: str) -> str:
        """Genera respuesta con contexto"""
        prompt = f"""
        Eres Heily, desarrolladora backend especializada en IA.
        Responde EN PRIMERA PERSONA.

        CONTEXTO:
        {context}

        PREGUNTA: {message}
        """

        try:
            # Nota: generate_content no es async por defecto en la SDK de Google, 
            # pero podemos envolverlo si fuera necesario.
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error en GeminiService: {str(e)}")
            return f"Error: {str(e)}"

gemini_service = GeminiService()

