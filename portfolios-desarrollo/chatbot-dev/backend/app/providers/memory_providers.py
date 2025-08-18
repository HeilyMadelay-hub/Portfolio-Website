import json
import time
import logging
from typing import List, Dict, Any, Optional
from ..interfaces import IVectorStore, ICacheProvider

logger = logging.getLogger(__name__)

class InMemoryVectorStore(IVectorStore):
    """Implementación de vector store en memoria"""
    
    def __init__(self):
        self.documents = []
        self.embeddings = []
        self.metadata = []
        logger.info("InMemoryVectorStore inicializado")
    
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]) -> bool:
        """Agrega documentos con embeddings"""
        try:
            if len(documents) != len(embeddings):
                logger.error("Cantidad de documentos y embeddings no coincide")
                return False
            
            for doc, embedding in zip(documents, embeddings):
                self.documents.append(doc.get('content', ''))
                self.embeddings.append(embedding)
                self.metadata.append(doc.get('metadata', {}))
            
            logger.info(f"Agregados {len(documents)} documentos al vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error agregando documentos: {e}")
            return False
    
    def search_similar(self, query_embedding: List[float], k: int) -> List[Dict]:
        """Busca documentos similares"""
        try:
            if not self.embeddings:
                return []
            
            similarities = []
            for i, doc_embedding in enumerate(self.embeddings):
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append((i, similarity))
            
            # Ordenar por similitud (mayor a menor)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Retornar top k
            results = []
            for i, similarity in similarities[:k]:
                results.append({
                    'content': self.documents[i],
                    'metadata': self.metadata[i],
                    'similarity': similarity
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error buscando similares: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas del store"""
        return {
            'total_documents': len(self.documents),
            'total_embeddings': len(self.embeddings),
            'store_type': 'in_memory'
        }
    
    def clear(self) -> bool:
        """Limpia el store"""
        try:
            self.documents = []
            self.embeddings = []
            self.metadata = []
            logger.info("Vector store limpiado")
            return True
        except Exception as e:
            logger.error(f"Error limpiando store: {e}")
            return False
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similitud coseno"""
        try:
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = sum(a * a for a in vec1) ** 0.5
            magnitude2 = sum(b * b for b in vec2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0
            
            return dot_product / (magnitude1 * magnitude2)
        except:
            return 0


class InMemoryCacheProvider(ICacheProvider):
    """Implementación de cache en memoria"""
    
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        logger.info("InMemoryCacheProvider inicializado")
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor del cache"""
        try:
            if key not in self.cache:
                return None
            
            # Verificar TTL
            timestamp, ttl = self.timestamps.get(key, (0, 0))
            if time.time() - timestamp > ttl:
                self.delete(key)
                return None
            
            return self.cache[key]
            
        except Exception as e:
            logger.error(f"Error obteniendo del cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Establece valor en cache"""
        try:
            self.cache[key] = value
            self.timestamps[key] = (time.time(), ttl)
            return True
        except Exception as e:
            logger.error(f"Error estableciendo cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Elimina del cache"""
        try:
            if key in self.cache:
                del self.cache[key]
            if key in self.timestamps:
                del self.timestamps[key]
            return True
        except Exception as e:
            logger.error(f"Error eliminando del cache: {e}")
            return False
    
    def clear(self) -> bool:
        """Limpia todo el cache"""
        try:
            self.cache = {}
            self.timestamps = {}
            logger.info("Cache limpiado")
            return True
        except Exception as e:
            logger.error(f"Error limpiando cache: {e}")
            return False
