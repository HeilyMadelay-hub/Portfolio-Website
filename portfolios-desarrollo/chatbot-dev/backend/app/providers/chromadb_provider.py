import chromadb
import os
import logging
from typing import List, Dict, Any, Optional
from ..interfaces import IVectorStore
from ..config.settings import Config

logger = logging.getLogger(__name__)

class ChromaDBVectorStore(IVectorStore):
    """Implementación de ChromaDB para vector store"""
    
    def __init__(self):
        try:
            # Asegurar que el directorio existe
            os.makedirs(Config.VECTORSTORE_DIR, exist_ok=True)
            
            # Configurar ChromaDB en modo persistente
            self.chroma_client = chromadb.PersistentClient(
                path=Config.VECTORSTORE_DIR
            )
            
            # Crear o obtener colección
            self.collection_name = "portfolio_documents"
            try:
                self.collection = self.chroma_client.get_collection(self.collection_name)
                logger.info(f"Colección '{self.collection_name}' cargada desde ChromaDB")
            except Exception:
                # Si no existe, crear nueva colección
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Portfolio documents for RAG"}
                )
                logger.info(f"Colección '{self.collection_name}' creada en ChromaDB")
            
            self._available = True
            logger.info("ChromaDB Vector Store inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error inicializando ChromaDB: {e}")
            self._available = False
            self.chroma_client = None
            self.collection = None
    
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]) -> bool:
        """Agrega documentos con embeddings a ChromaDB"""
        try:
            if not self._available or not self.collection:
                logger.error("ChromaDB no disponible")
                return False

            if len(documents) != len(embeddings):
                logger.error("Cantidad de documentos y embeddings no coincide")
                return False

            # Preparar datos para ChromaDB
            texts = []
            ids = []
            metadatas = []
            chroma_embeddings = []

            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                if not embedding:  # Skip documentos sin embedding
                    continue

                # Generar ID único
                doc_id = f"doc_{i}_{doc.get('metadata', {}).get('filename', 'unknown')}"

                texts.append(doc['content'])
                ids.append(doc_id)
                metadatas.append(doc.get('metadata', {}))
                chroma_embeddings.append(embedding)

            if not chroma_embeddings:
                logger.warning("No hay embeddings válidos para agregar")
                return False

            # Agregar a ChromaDB
            self.collection.add(
                documents=texts,
                embeddings=chroma_embeddings,
                ids=ids,
                metadatas=metadatas
            )

            # Instrumentación: intentar incrementar contador de requests/ops
            try:
                from ..monitoring.prometheus_exporter import inc_request
                if inc_request:
                    inc_request(endpoint='chromadb_add_documents', method='ADD')
            except Exception:
                pass

            logger.info(f"Agregados {len(chroma_embeddings)} documentos a ChromaDB")
            return True

        except Exception as e:
            logger.error(f"Error agregando documentos a ChromaDB: {e}")
            # Instrumentación: error en provider
            try:
                from ..monitoring.prometheus_exporter import inc_error
                if inc_error:
                    inc_error(endpoint='chromadb_add_documents', err_type=type(e).__name__)
            except Exception:
                pass
            return False
    
    def search_similar(self, query_embedding: List[float], k: int) -> List[Dict]:
        """Busca documentos similares en ChromaDB"""
        try:
            if not self._available or not self.collection:
                logger.error("ChromaDB no disponible para búsqueda")
                return []
            
            if not query_embedding:
                logger.error("Query embedding vacío")
                return []
            
            # Buscar en ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, 10)  # Limitar máximo a 10
            )
            
            # Formatear resultados
            similar_docs = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    similar_doc = {
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else 0,
                        'similarity': 1 - (results['distances'][0][i] if results['distances'] and results['distances'][0] else 0)
                    }
                    similar_docs.append(similar_doc)
            
            logger.info(f"ChromaDB encontró {len(similar_docs)} documentos similares")
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error buscando en ChromaDB: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de ChromaDB"""
        try:
            if not self._available or not self.collection:
                return {
                    'total_documents': 0,
                    'store_type': 'chromadb',
                    'available': False,
                    'error': 'ChromaDB not available'
                }
            
            count = self.collection.count()
            return {
                'total_documents': count,
                'store_type': 'chromadb',
                'collection_name': self.collection_name,
                'available': True,
                'storage_path': Config.VECTORSTORE_DIR
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo stats de ChromaDB: {e}")
            return {
                'total_documents': 0,
                'store_type': 'chromadb',
                'available': False,
                'error': str(e)
            }
    
    def clear(self) -> bool:
        """Limpia todos los documentos de ChromaDB"""
        try:
            if not self._available or not self.chroma_client:
                logger.error("ChromaDB no disponible para limpiar")
                return False
            
            # Eliminar colección existente
            try:
                self.chroma_client.delete_collection(self.collection_name)
                logger.info(f"Colección '{self.collection_name}' eliminada")
            except Exception as e:
                logger.warning(f"Error eliminando colección: {e}")
            
            # Crear nueva colección vacía
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Portfolio documents for RAG"}
            )
            
            logger.info("ChromaDB limpiado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando ChromaDB: {e}")
            return False
    
    def is_available(self) -> bool:
        """Verifica si ChromaDB está disponible"""
        return self._available
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Información detallada de la colección"""
        try:
            if not self._available or not self.collection:
                return {'error': 'ChromaDB not available'}
            
            return {
                'name': self.collection_name,
                'count': self.collection.count(),
                'metadata': getattr(self.collection, 'metadata', {}),
                'storage_path': Config.VECTORSTORE_DIR
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo info de colección: {e}")
            return {'error': str(e)}
