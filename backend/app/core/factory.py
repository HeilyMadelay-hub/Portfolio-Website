import logging
from typing import Dict, Any, Optional
from ..interfaces import ILLMProvider, IEmbeddingProvider, IVectorStore, IDocumentProcessor, ICacheProvider
from ..providers import (
    GeminiLLMProvider, 
    GeminiEmbeddingProvider, 
    InMemoryVectorStore, 
    InMemoryCacheProvider,
    FileSystemDocumentProcessor
)

# Importar ChromaDB provider
try:
    from ..providers.chromadb_provider import ChromaDBVectorStore
    CHROMADB_AVAILABLE = True
except ImportError as e:
    logger.warning(f"ChromaDB no disponible: {e}")
    CHROMADB_AVAILABLE = False

from ..config.settings import Config

logger = logging.getLogger(__name__)

class ProviderFactory:
    """Factory para crear proveedores con acoplamiento débil"""
    
    @staticmethod
    def create_llm_provider(provider_type: str = "gemini") -> Optional[ILLMProvider]:
        """Crea proveedor de LLM"""
        try:
            if provider_type.lower() == "gemini":
                return GeminiLLMProvider()
            else:
                logger.error(f"Proveedor LLM no soportado: {provider_type}")
                return None
        except Exception as e:
            logger.error(f"Error creando LLM provider: {e}")
            return None
    
    @staticmethod
    def create_embedding_provider(provider_type: str = "gemini") -> Optional[IEmbeddingProvider]:
        """Crea proveedor de embeddings"""
        try:
            if provider_type.lower() == "gemini":
                return GeminiEmbeddingProvider()
            else:
                logger.error(f"Proveedor embedding no soportado: {provider_type}")
                return None
        except Exception as e:
            logger.error(f"Error creando embedding provider: {e}")
            return None
    
    @staticmethod
    def create_vector_store(store_type: str = "chromadb") -> Optional[IVectorStore]:  # ✅ Cambiar default a chromadb
        """Crea almacén vectorial"""
        try:
            if store_type.lower() == "chromadb":
                if CHROMADB_AVAILABLE:
                    return ChromaDBVectorStore()
                else:
                    logger.warning("ChromaDB no disponible, usando memoria")
                    return InMemoryVectorStore()
            elif store_type.lower() == "memory":
                return InMemoryVectorStore()
            else:
                logger.error(f"Vector store no soportado: {store_type}")
                return None
        except Exception as e:
            logger.error(f"Error creando vector store: {e}")
            # Fallback a memoria si ChromaDB falla
            if store_type.lower() == "chromadb":
                logger.info("Fallback a InMemoryVectorStore")
                return InMemoryVectorStore()
            return None
    
    @staticmethod
    def create_document_processor(processor_type: str = "filesystem") -> Optional[IDocumentProcessor]:
        """Crea procesador de documentos"""
        try:
            if processor_type.lower() == "filesystem":
                return FileSystemDocumentProcessor()
            else:
                logger.error(f"Document processor no soportado: {processor_type}")
                return None
        except Exception as e:
            logger.error(f"Error creando document processor: {e}")
            return None
    
    @staticmethod
    def create_cache_provider(cache_type: str = "memory") -> Optional[ICacheProvider]:
        """Crea proveedor de cache"""
        try:
            if cache_type.lower() == "memory":
                return InMemoryCacheProvider()
            # Aquí se pueden agregar: redis, memcached, etc.
            else:
                logger.error(f"Cache provider no soportado: {cache_type}")
                return None
        except Exception as e:
            logger.error(f"Error creando cache provider: {e}")
            return None
    
    @staticmethod
    def create_all_providers(config: Dict[str, str] = None) -> Dict[str, Any]:
        """Crea todos los proveedores según configuración"""
        if config is None:
            config = {
                'llm': 'gemini',
                'embedding': 'gemini', 
                'vector_store': 'chromadb',  # ✅ Cambiar default a chromadb
                'document_processor': 'filesystem',
                'cache': 'memory'
            }
        
        providers = {}
        
        # Crear cada proveedor
        providers['llm'] = ProviderFactory.create_llm_provider(config.get('llm', 'gemini'))
        providers['embedding'] = ProviderFactory.create_embedding_provider(config.get('embedding', 'gemini'))
        providers['vector_store'] = ProviderFactory.create_vector_store(config.get('vector_store', 'chromadb'))
        providers['document_processor'] = ProviderFactory.create_document_processor(config.get('document_processor', 'filesystem'))
        providers['cache'] = ProviderFactory.create_cache_provider(config.get('cache', 'memory'))
        
        # Verificar que todos se crearon correctamente
        failed_providers = [name for name, provider in providers.items() if provider is None]
        if failed_providers:
            logger.warning(f"Proveedores fallidos: {failed_providers}")
        
        successful_providers = [name for name, provider in providers.items() if provider is not None]
        logger.info(f"Proveedores creados exitosamente: {successful_providers}")
        
        # Información de vector store usado
        vector_store = providers.get('vector_store')
        if vector_store:
            store_type = vector_store.__class__.__name__
            logger.info(f"Vector Store activo: {store_type}")
        
        return providers
