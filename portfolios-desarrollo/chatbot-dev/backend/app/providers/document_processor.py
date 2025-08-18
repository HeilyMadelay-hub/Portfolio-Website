import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import PyPDF2
import docx
from ..interfaces import IDocumentProcessor
from ..config.settings import Config

logger = logging.getLogger(__name__)

class FileSystemDocumentProcessor(IDocumentProcessor):
    """Procesador de documentos desde sistema de archivos"""
    
    def __init__(self):
        self.documents_dir = Config.DOCUMENTS_DIR
        self.supported_formats = ['.pdf', '.docx', '.txt', '.md']
        
        # Directorios específicos
        self.base_dirs = [
            os.path.join(self.documents_dir, 'datos_base_es'),
            os.path.join(self.documents_dir, 'datos_base_traducidos'),
            self.documents_dir
        ]
        
        logger.info(f"DocumentProcessor inicializado: {len(self.base_dirs)} directorios")
    
    def load_documents(self) -> List[Dict[str, Any]]:
        """Carga todos los documentos"""
        all_documents = []
        
        try:
            for base_dir in self.base_dirs:
                if os.path.exists(base_dir):
                    documents = self._load_from_directory(base_dir)
                    all_documents.extend(documents)
            
            logger.info(f"Cargados {len(all_documents)} documentos total")
            
        except Exception as e:
            logger.error(f"Error cargando documentos: {e}")
        
        return all_documents
    
    def get_supported_formats(self) -> List[str]:
        """Formatos soportados"""
        return self.supported_formats.copy()
    
    def process_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Procesa un texto y lo divide en chunks"""
        import re
        
        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Si el texto es más corto que el tamaño del chunk, devolverlo como está
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Determinar el final del chunk
            end = start + chunk_size
            
            if end >= len(text):
                # Si es el último chunk, tomar hasta el final
                chunk = text[start:]
            else:
                # Buscar el último espacio antes del límite
                last_space = text.rfind(' ', start, end)
                if last_space != -1:
                    end = last_space
                chunk = text[start:end]
            
            # Añadir el chunk
            if chunk.strip():
                chunks.append(chunk.strip())
            
            # Mover el inicio teniendo en cuenta el overlap
            start = end - chunk_overlap if end < len(text) else len(text)
        
        return chunks
    
    def get_documents_info(self) -> Dict[str, Any]:
        """Información de documentos"""
        try:
            info = {
                'base_directories': self.base_dirs,
                'supported_formats': self.supported_formats,
                'directories_info': {},
                'total_files': 0
            }
            
            for base_dir in self.base_dirs:
                if os.path.exists(base_dir):
                    dir_info = self._analyze_directory(base_dir)
                    info['directories_info'][os.path.basename(base_dir)] = dir_info
                    info['total_files'] += dir_info['file_count']
            
            return info
            
        except Exception as e:
            logger.error(f"Error obteniendo info: {e}")
            return {'error': str(e)}
    
    def _load_from_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Carga desde directorio específico"""
        documents = []
        
        try:
            for file_path in Path(directory).rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                    docs = self._process_file(file_path)
                    if docs:
                        documents.extend(docs if isinstance(docs, list) else [docs])
            
            logger.info(f"Cargados {len(documents)} desde {directory}")
            
        except Exception as e:
            logger.error(f"Error en directorio {directory}: {e}")
        
        return documents
    
    def _process_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Procesa archivo individual"""
        try:
            content = ""
            file_extension = file_path.suffix.lower()
            
            if file_extension == '.pdf':
                content = self._read_pdf(file_path)
            elif file_extension == '.docx':
                content = self._read_docx(file_path)
            elif file_extension in ['.txt', '.md']:
                content = self._read_text(file_path)
            
            if not content:
                return []
            
            chunks = self._split_content(content)
            documents = []
            
            for i, chunk in enumerate(chunks):
                doc = {
                    'content': chunk,
                    'metadata': {
                        'filename': file_path.name,
                        'file_type': file_extension,
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'directory': file_path.parent.name,
                        'full_path': str(file_path)
                    }
                }
                documents.append(doc)
            
            return documents
                
        except Exception as e:
            logger.error(f"Error procesando {file_path}: {e}")
            return []
    
    def _read_pdf(self, file_path: Path) -> str:
        """Lee PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
                return content.strip()
        except Exception as e:
            logger.error(f"Error leyendo PDF {file_path}: {e}")
            return ""
    
    def _read_docx(self, file_path: Path) -> str:
        """Lee DOCX"""
        try:
            doc = docx.Document(file_path)
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
            return content.strip()
        except Exception as e:
            logger.error(f"Error leyendo DOCX {file_path}: {e}")
            return ""
    
    def _read_text(self, file_path: Path) -> str:
        """Lee texto"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read().strip()
            except Exception as e:
                logger.error(f"Error leyendo texto {file_path}: {e}")
                return ""
        except Exception as e:
            logger.error(f"Error leyendo texto {file_path}: {e}")
            return ""
    
    def _split_content(self, content: str) -> List[str]:
        """Divide en chunks"""
        if len(content) <= Config.CHUNK_SIZE:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + Config.CHUNK_SIZE
            
            if end < len(content):
                last_space = content.rfind(' ', start, end)
                last_newline = content.rfind('\n', start, end)
                last_period = content.rfind('.', start, end)
                
                cut_point = max(last_space, last_newline, last_period)
                if cut_point > start:
                    end = cut_point + (1 if content[cut_point] == '.' else 0)
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - Config.CHUNK_OVERLAP if end < len(content) else end
        
        return chunks
    
    def _analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analiza directorio"""
        try:
            files = []
            for file_path in Path(directory).rglob('*'):
                if file_path.is_file():
                    files.append({
                        'name': file_path.name,
                        'extension': file_path.suffix.lower(),
                        'size_bytes': file_path.stat().st_size,
                        'supported': file_path.suffix.lower() in self.supported_formats
                    })
            
            return {
                'path': directory,
                'files': files,
                'file_count': len(files)
            }
        except Exception as e:
            logger.error(f"Error analizando {directory}: {e}")
            return {'path': directory, 'files': [], 'file_count': 0}
