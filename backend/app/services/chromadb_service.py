import logging
import os
from typing import List, Optional
from ..providers.chromadb_provider import ChromaDBVectorStore
from ..providers.gemini_provider import GeminiEmbeddingProvider

logger = logging.getLogger(__name__)

class ChromaDBService:
    def __init__(self):
        self.vector_store = ChromaDBVectorStore()
        self.embedding_provider = GeminiEmbeddingProvider()
        logger.info("✅ ChromaDBService inicializado")

    def load_documents(self):
        """Carga documentos iniciales si es necesario"""
        logger.info("Cargando documentos en ChromaDB...")
        # Aquí se podría llamar a un script de población o cargar archivos locales
        pass

    def search(self, query: str, n_results: int = 3) -> str:
        """Busca contexto relevante para una consulta"""
        try:
            # 1. Generar embedding para la consulta
            query_embedding = self.embedding_provider.generate_embedding(query)
            if not query_embedding:
                logger.warning("No se pudo generar embedding para la consulta")
                return ""

            # 2. Buscar en el vector store
            results = self.vector_store.search_similar(query_embedding, k=n_results)
            
            if results:
                # Unir los contenidos encontrados
                context = "\n\n".join([doc['content'] for doc in results])
                return context
            
            return "No se encontró contexto relevante."
        except Exception as e:
            logger.error(f"Error buscando en ChromaDB: {e}")
            return ""

chromadb_service = ChromaDBService()

