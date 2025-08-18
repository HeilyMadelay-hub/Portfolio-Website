import re
import html
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SanitizationConfig:
    """Configuración para sanitización de entrada"""
    max_length: int = 500  # Según diagrama: Longitud > 500?
    min_length: int = 1
    allowed_chars_pattern: str = r'[a-zA-Z0-9\s\.,\?!¿¡áéíóúüñÁÉÍÓÚÜÑ\-\(\)\/\:;]'
    blocked_patterns: List[str] = None
    
    def __post_init__(self):
        if self.blocked_patterns is None:
            # Patrones bloqueados por defecto
            self.blocked_patterns = [
                r'<script.*?>.*?</script>',  # Scripts
                r'javascript:',              # JavaScript URLs
                r'data:.*base64',           # Data URLs base64
                r'eval\(',                  # Eval calls
                r'exec\(',                  # Exec calls
                r'import\s+',               # Import statements
                r'__.*__',                  # Python dunders
            ]

class InputSanitizer:
    """
    Sanitizador de entrada según diagrama híbrido
    Implementa: PROC_INPUT -> TRUNC -> SANITIZE
    """
    
    def __init__(self, config: Optional[SanitizationConfig] = None):
        self.config = config or SanitizationConfig()
        
        # Compilar patrones regex para optimización
        self.blocked_regex = [re.compile(pattern, re.IGNORECASE) for pattern in self.config.blocked_patterns]
        self.allowed_chars_regex = re.compile(self.config.allowed_chars_pattern)
        
        logger.info(f"InputSanitizer inicializado: max_length={self.config.max_length}")
    
    def process_input(self, message: str, user_context: str = None) -> Dict[str, any]:
        """
        Procesa entrada según el diagrama de flujo:
        PROC_INPUT -> TRUNC{Longitud > 500?} -> TRUNCATE/SANITIZE
        
        Args:
            message: Mensaje del usuario
            user_context: Contexto adicional (opcional)
        
        Returns:
            Dict con processed_message, warnings, is_valid
        """
        try:
            result = {
                'processed_message': '',
                'original_length': len(message),
                'warnings': [],
                'is_valid': True,
                'transformations': []
            }
            
            # Paso 1: Validación inicial
            validation_result = self._validate_input(message)
            if not validation_result['is_valid']:
                result.update(validation_result)
                return result
            
            # Paso 2: Truncamiento (según diagrama)
            truncated_message, was_truncated = self._truncate_message(message)
            if was_truncated:
                result['warnings'].append(f"Mensaje truncado de {len(message)} a {len(truncated_message)} caracteres")
                result['transformations'].append('truncated')
            
            # Paso 3: Sanitización
            sanitized_message, sanitization_warnings = self._sanitize_message(truncated_message)
            result['warnings'].extend(sanitization_warnings)
            
            # Paso 4: Normalización
            normalized_message = self._normalize_message(sanitized_message)
            
            result['processed_message'] = normalized_message
            result['final_length'] = len(normalized_message)
            
            # Validación final
            if not normalized_message.strip():
                result['is_valid'] = False
                result['warnings'].append("Mensaje vacío después del procesamiento")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando entrada: {e}")
            return {
                'processed_message': '',
                'is_valid': False,
                'error': str(e),
                'warnings': ['Error durante el procesamiento']
            }
    
    def _validate_input(self, message: str) -> Dict[str, any]:
        """Validación inicial de entrada"""
        warnings = []
        
        # Verificar longitud mínima
        if len(message) < self.config.min_length:
            return {
                'is_valid': False,
                'warnings': ['Mensaje muy corto'],
                'error': 'Mensaje debe tener al menos 1 caracter'
            }
        
        # Verificar patrones bloqueados
        for pattern_regex in self.blocked_regex:
            if pattern_regex.search(message):
                logger.warning(f"Patrón bloqueado detectado: {pattern_regex.pattern}")
                return {
                    'is_valid': False,
                    'warnings': ['Contenido no permitido detectado'],
                    'error': 'Mensaje contiene patrones no permitidos'
                }
        
        # Verificar caracteres sospechosos
        suspicious_chars = len(message) - len(re.findall(self.allowed_chars_regex, message))
        if suspicious_chars > len(message) * 0.3:  # Más del 30% caracteres raros
            warnings.append(f"Detectados {suspicious_chars} caracteres sospechosos")
        
        return {
            'is_valid': True,
            'warnings': warnings
        }
    
    def _truncate_message(self, message: str) -> tuple[str, bool]:
        """
        Trunca mensaje según diagrama: Longitud > 500? -> TRUNCATE
        """
        if len(message) <= self.config.max_length:
            return message, False
        
        # Truncar intentando mantener palabras completas
        truncated = message[:self.config.max_length]
        
        # Buscar último espacio para no cortar palabras
        last_space = truncated.rfind(' ')
        if last_space > self.config.max_length * 0.8:  # Si está en el último 20%
            truncated = truncated[:last_space]
        
        # Evitar truncar en medio de una oración
        sentence_endings = ['.', '!', '?']
        for i in range(len(truncated) - 1, max(0, len(truncated) - 50), -1):
            if truncated[i] in sentence_endings:
                truncated = truncated[:i + 1]
                break
        
        logger.info(f"Mensaje truncado de {len(message)} a {len(truncated)} caracteres")
        return truncated, True
    
    def _sanitize_message(self, message: str) -> tuple[str, List[str]]:
        """Sanitiza mensaje removiendo contenido peligroso"""
        warnings = []
        sanitized = message
        
        # 1. Escape HTML
        original_length = len(sanitized)
        sanitized = html.escape(sanitized)
        if len(sanitized) != original_length:
            warnings.append("HTML escapado")
        
        # 2. Remover URLs sospechosas
        url_patterns = [
            r'https?://[^\s]+',  # URLs HTTP
            r'ftp://[^\s]+',     # URLs FTP
            r'www\.[^\s]+',      # URLs www
        ]
        
        for pattern in url_patterns:
            matches = re.findall(pattern, sanitized, re.IGNORECASE)
            if matches:
                warnings.append(f"URLs removidas: {len(matches)}")
                sanitized = re.sub(pattern, '[URL_REMOVIDA]', sanitized, flags=re.IGNORECASE)
        
        # 3. Remover caracteres de control
        control_chars = re.findall(r'[\x00-\x1f\x7f-\x9f]', sanitized)
        if control_chars:
            warnings.append(f"Caracteres de control removidos: {len(control_chars)}")
            sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
        
        # 4. Limpiar exceso de espacios/saltos de línea
        original_sanitized = sanitized
        sanitized = re.sub(r'\s+', ' ', sanitized)  # Múltiples espacios -> uno
        sanitized = re.sub(r'\n+', '\n', sanitized)  # Múltiples saltos -> uno
        
        if sanitized != original_sanitized:
            warnings.append("Espacios normalizados")
        
        return sanitized, warnings
    
    def _normalize_message(self, message: str) -> str:
        """Normalización final del mensaje"""
        # Aplicar normalización Unicode NFKC
        try:
            import unicodedata
            message = unicodedata.normalize('NFKC', message)
        except Exception:
            pass

        # Mapear homoglyphs comunes básicos (ejemplo: sustituir caracteres confusos por equivalentes ASCII)
        homoglyph_map = {
            '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
            '\u2013': '-', '\u2014': '-', '\u00a0': ' ', '\u2026': '...'
        }
        try:
            for k, v in homoglyph_map.items():
                message = message.replace(k, v)
        except Exception:
            pass

        # Trim espacios al inicio y final
        normalized = message.strip()
        
        # Capitalizar primera letra si es necesario
        if normalized and normalized[0].islower():
            normalized = normalized[0].upper() + normalized[1:]
        
        # Asegurar que termine con puntuación
        if normalized and normalized[-1] not in '.!?':
            normalized += '.'
        
        return normalized
    
    def validate_processed_input(self, processed_message: str) -> Dict[str, any]:
        """Validación final del mensaje procesado"""
        try:
            issues = []
            
            # Verificar longitud final
            if len(processed_message) < self.config.min_length:
                issues.append("Mensaje muy corto después del procesamiento")
            
            if len(processed_message) > self.config.max_length:
                issues.append("Mensaje aún muy largo después del procesamiento")
            
            # Verificar contenido significativo
            content_ratio = len(processed_message.replace(' ', '')) / len(processed_message) if processed_message else 0
            if content_ratio < 0.1:  # Menos del 10% es contenido
                issues.append("Muy poco contenido significativo")
            
            # Verificar que no sea solo puntuación
            alpha_chars = sum(1 for c in processed_message if c.isalnum())
            if alpha_chars < 3:
                issues.append("Muy pocos caracteres alfanuméricos")
            
            return {
                'is_valid': len(issues) == 0,
                'issues': issues,
                'content_ratio': content_ratio,
                'alpha_chars': alpha_chars
            }
            
        except Exception as e:
            logger.error(f"Error en validación final: {e}")
            return {
                'is_valid': False,
                'issues': ['Error en validación final'],
                'error': str(e)
            }
    
    def get_stats(self) -> Dict[str, any]:
        """Estadísticas del sanitizador"""
        return {
            'config': {
                'max_length': self.config.max_length,
                'min_length': self.config.min_length,
                'blocked_patterns_count': len(self.config.blocked_patterns)
            },
            'processor_status': 'active'
        }

# Instancia global del sanitizador
input_sanitizer = InputSanitizer()

def process_user_input(message: str, user_context: str = None) -> Dict[str, any]:
    """Función helper para procesar entrada del usuario"""
    return input_sanitizer.process_input(message, user_context)

def validate_input_safety(message: str) -> bool:
    """Validación rápida de seguridad de entrada"""
    try:
        result = input_sanitizer._validate_input(message)
        return result['is_valid']
    except Exception:
        return False
