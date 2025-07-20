from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import logging
from ..config.settings import Config

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Servicio para manejar embeddings y búsqueda vectorial con RAG"""
    
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=Config.EMBEDDING_MODEL,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
        
        self.vectorstore = self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Inicializa o carga el vectorstore existente"""
        try:
            # Verificar si ya existe el vectorstore
            if os.path.exists(Config.VECTORSTORE_DIR) and os.listdir(Config.VECTORSTORE_DIR):
                logger.info("Cargando vectorstore existente...")
                return Chroma(
                    persist_directory=Config.VECTORSTORE_DIR,
                    embedding_function=self.embeddings
                )
            else:
                logger.info("Creando nuevo vectorstore...")
                return Chroma(
                    persist_directory=Config.VECTORSTORE_DIR,
                    embedding_function=self.embeddings
                )
        except Exception as e:
            logger.error(f"Error inicializando vectorstore: {e}")
            raise
    
    def add_documents(self, documents):
        """Agrega documentos al vectorstore"""
        try:
            # Dividir documentos en chunks
            docs = self.text_splitter.split_documents(documents)
            
            # Agregar al vectorstore
            self.vectorstore.add_documents(docs)
            
            # Persistir cambios
            self.vectorstore.persist()
            
            logger.info(f"Agregados {len(docs)} chunks al vectorstore")
            return True
        except Exception as e:
            logger.error(f"Error agregando documentos: {e}")
            return False
    
    def search_similar(self, query, k=None):
        """Busca documentos similares a la consulta"""
        try:
            k = k or Config.SIMILARITY_TOP_K
            results = self.vectorstore.similarity_search(query, k=k)
            
            # Formatear resultados
            context_texts = []
            for doc in results:
                context_texts.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata
                })
            
            return context_texts
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return []
    
    def get_vectorstore_stats(self):
        """Retorna estadísticas del vectorstore"""
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                'total_documents': count,
                'vectorstore_path': Config.VECTORSTORE_DIR
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {'error': str(e)}