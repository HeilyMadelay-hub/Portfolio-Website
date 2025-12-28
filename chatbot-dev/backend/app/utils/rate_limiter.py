import time
import logging
from collections import defaultdict, deque
from typing import Dict, Optional
from dataclasses import dataclass
from ..config.settings import Config

logger = logging.getLogger(__name__)

@dataclass
class RateLimitConfig:
    """Configuración de rate limiting"""
    max_requests: int = 30  # Máximo requests por ventana
    window_seconds: int = 60  # Ventana de tiempo en segundos
    burst_limit: int = 5  # Límite de ráfaga
    burst_window: int = 10  # Ventana de ráfaga en segundos

class RateLimiter:
    """
    Rate Limiter según arquitectura híbrida
    Implementa ventanas deslizantes y límites de ráfaga
    """
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        
        # Almacén de timestamps por identificador
        self.requests: Dict[str, deque] = defaultdict(lambda: deque())
        self.burst_requests: Dict[str, deque] = defaultdict(lambda: deque())
        
        # Cache de decisiones para optimizar
        self.decision_cache: Dict[str, tuple] = {}
        
        logger.info(f"RateLimiter inicializado: {self.config.max_requests} req/{self.config.window_seconds}s")
    
    def is_allowed(self, identifier: str, request_type: str = "default") -> Dict[str, any]:
        """
        Verifica si una request está permitida según el diagrama de flujo
        
        Args:
            identifier: IP o user ID
            request_type: Tipo de request (chat, health, etc.)
        
        Returns:
            Dict con allowed, remaining, reset_time
        """
        try:
            current_time = time.time()
            
            # Limpiar requests antiguos
            self._cleanup_old_requests(identifier, current_time)
            
            # Verificar límite de ráfaga primero
            if not self._check_burst_limit(identifier, current_time):
                return {
                    'allowed': False,
                    'reason': 'burst_limit_exceeded',
                    'remaining': 0,
                    'reset_time': self._get_burst_reset_time(identifier, current_time),
                    'retry_after': self.config.burst_window
                }
            
            # Verificar límite principal
            requests_count = len(self.requests[identifier])
            
            if requests_count >= self.config.max_requests:
                return {
                    'allowed': False,
                    'reason': 'rate_limit_exceeded',
                    'remaining': 0,
                    'reset_time': self._get_reset_time(identifier, current_time),
                    'retry_after': self._calculate_retry_after(identifier, current_time)
                }
            
            # Request permitida - registrar timestamp
            self.requests[identifier].append(current_time)
            self.burst_requests[identifier].append(current_time)
            
            remaining = max(0, self.config.max_requests - len(self.requests[identifier]))
            
            return {
                'allowed': True,
                'remaining': remaining,
                'reset_time': current_time + self.config.window_seconds,
                'limit': self.config.max_requests
            }
            
        except Exception as e:
            logger.error(f"Error en rate limiting para {identifier}: {e}")
            # En caso de error, permitir la request (fail-open)
            return {
                'allowed': True,
                'remaining': self.config.max_requests,
                'reset_time': current_time + self.config.window_seconds,
                'error': str(e)
            }
    
    def _cleanup_old_requests(self, identifier: str, current_time: float):
        """Limpia requests fuera de la ventana de tiempo"""
        # Limpiar ventana principal
        window_start = current_time - self.config.window_seconds
        requests = self.requests[identifier]
        
        while requests and requests[0] <= window_start:
            requests.popleft()
        
        # Limpiar ventana de ráfaga
        burst_window_start = current_time - self.config.burst_window
        burst_requests = self.burst_requests[identifier]
        
        while burst_requests and burst_requests[0] <= burst_window_start:
            burst_requests.popleft()
    
    def _check_burst_limit(self, identifier: str, current_time: float) -> bool:
        """Verifica límite de ráfaga"""
        burst_count = len(self.burst_requests[identifier])
        return burst_count < self.config.burst_limit
    
    def _get_reset_time(self, identifier: str, current_time: float) -> float:
        """Calcula cuándo se resetea el límite principal"""
        requests = self.requests[identifier]
        if not requests:
            return current_time
        
        oldest_request = requests[0]
        return oldest_request + self.config.window_seconds
    
    def _get_burst_reset_time(self, identifier: str, current_time: float) -> float:
        """Calcula cuándo se resetea el límite de ráfaga"""
        burst_requests = self.burst_requests[identifier]
        if not burst_requests:
            return current_time
        
        oldest_burst = burst_requests[0]
        return oldest_burst + self.config.burst_window
    
    def _calculate_retry_after(self, identifier: str, current_time: float) -> int:
        """Calcula segundos hasta que se permita la siguiente request"""
        reset_time = self._get_reset_time(identifier, current_time)
        return max(1, int(reset_time - current_time))
    
    def get_stats(self, identifier: str) -> Dict[str, any]:
        """Obtiene estadísticas de rate limiting para un identificador"""
        try:
            current_time = time.time()
            self._cleanup_old_requests(identifier, current_time)
            
            return {
                'current_requests': len(self.requests[identifier]),
                'max_requests': self.config.max_requests,
                'window_seconds': self.config.window_seconds,
                'burst_requests': len(self.burst_requests[identifier]),
                'burst_limit': self.config.burst_limit,
                'reset_time': self._get_reset_time(identifier, current_time)
            }
        except Exception as e:
            logger.error(f"Error obteniendo stats para {identifier}: {e}")
            return {'error': str(e)}
    
    def reset_user_limits(self, identifier: str):
        """Resetea límites para un usuario específico (admin function)"""
        try:
            if identifier in self.requests:
                del self.requests[identifier]
            if identifier in self.burst_requests:
                del self.burst_requests[identifier]
            
            logger.info(f"Rate limits reseteados para {identifier}")
            return True
        except Exception as e:
            logger.error(f"Error reseteando límites para {identifier}: {e}")
            return False
    
    def get_global_stats(self) -> Dict[str, any]:
        """Estadísticas globales del rate limiter"""
        try:
            current_time = time.time()
            
            # Limpiar todos los usuarios
            for identifier in list(self.requests.keys()):
                self._cleanup_old_requests(identifier, current_time)
            
            # Eliminar usuarios sin requests
            empty_users = [
                identifier for identifier, requests in self.requests.items()
                if not requests
            ]
            for identifier in empty_users:
                del self.requests[identifier]
                if identifier in self.burst_requests:
                    del self.burst_requests[identifier]
            
            total_active_users = len(self.requests)
            total_requests = sum(len(requests) for requests in self.requests.values())
            
            return {
                'active_users': total_active_users,
                'total_requests_in_window': total_requests,
                'config': {
                    'max_requests': self.config.max_requests,
                    'window_seconds': self.config.window_seconds,
                    'burst_limit': self.config.burst_limit,
                    'burst_window': self.config.burst_window
                }
            }
        except Exception as e:
            logger.error(f"Error obteniendo stats globales: {e}")
            return {'error': str(e)}

# Instancia global del rate limiter
rate_limiter = RateLimiter()

def check_rate_limit(identifier: str, request_type: str = "default") -> Dict[str, any]:
    """Función helper para verificar rate limiting"""
    return rate_limiter.is_allowed(identifier, request_type)

def get_client_identifier(request) -> str:
    """Extrae identificador del cliente desde la request"""
    # Intentar obtener IP real detrás de proxies
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip
    
    return request.remote_addr or 'unknown'
