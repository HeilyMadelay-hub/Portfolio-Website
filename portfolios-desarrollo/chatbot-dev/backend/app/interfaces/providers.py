from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class ILLMProvider(ABC):
    """Interfaz para proveedores de LLM (Language Learning Models)"""
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Genera una respuesta usando el LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica si el proveedor está disponible"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        """Retorna información del modelo"""
        pass


class IEmbeddingProvider(ABC):
    """Interfaz para proveedores de embeddings"""
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Genera embedding de un texto"""
        pass
    
    @abstractmethod
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Genera embeddings de múltiples textos"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica si el proveedor está disponible"""
        pass


class IVectorStore(ABC):
    """Interfaz para almacenes vectoriales"""
    
    @abstractmethod
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]) -> bool:
        """Agrega documentos con sus embeddings"""
        pass
    
    @abstractmethod
    def search_similar(self, query_embedding: List[float], k: int) -> List[Dict]:
        """Busca documentos similares"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del store"""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """Limpia el store"""
        pass


class IDocumentProcessor(ABC):
    """Interfaz para procesadores de documentos"""
    
    @abstractmethod
    def load_documents(self) -> List[Dict[str, Any]]:
        """Carga documentos desde la fuente"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Retorna formatos soportados"""
        pass
    
    @abstractmethod
    def get_documents_info(self) -> Dict[str, Any]:
        """Obtiene información de documentos disponibles"""
        pass


class ICacheProvider(ABC):
    """Interfaz para proveedores de cache"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor del cache"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Establece valor en cache"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Elimina valor del cache"""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """Limpia todo el cache"""
        pass
