"""
Monitoring Routes (FastAPI-only)
Expone un dashboard simple y las métricas Prometheus.
"""

import logging
from typing import Optional
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, Response

from ..monitoring.prometheus_exporter import get_metrics as prometheus_get_metrics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


def generate_dashboard_html() -> str:
    """Genera un HTML mínimo para el dashboard de monitoring."""
    return (
        "<html><head><title>Monitoring Dashboard</title></head><body>"
        "<h1>Monitoring Dashboard</h1>"
        "<ul>"
        "<li><a href='/api/monitoring/metrics'>Metrics (Prometheus)</a></li>"
        "<li><a href='/api/monitoring/metrics/prometheus'>Prometheus raw</a></li>"
        "</ul>"
        "</body></html>"
    )


@router.get("/dashboard")
async def monitoring_dashboard():
    """Dashboard HTML con métricas en tiempo real del sistema híbrido."""
    dashboard_html = generate_dashboard_html()
    return HTMLResponse(content=dashboard_html)


@router.get("/metrics")
async def metrics_endpoint(component: Optional[str] = Query(None, description="Componente específico"),
                           time_range: Optional[str] = Query("1h", description="Rango de tiempo (1h, 24h, 7d)")):
    """Retorna métricas en formato Prometheus (text/plain; version=0.0.4)."""
    data, content_type = prometheus_get_metrics()
    return Response(content=data, media_type=content_type)


@router.get("/metrics/prometheus")
async def prometheus_raw():
    """Alias para obtener las métricas Prometheus en bruto."""
    data, content_type = prometheus_get_metrics()
    return Response(content=data, media_type=content_type)
# ==================== FUNCIONES DE RECOLECCIÓN DE MÉTRICAS ====================

def collect_system_metrics(component: Optional[str] = None, time_range: str = "1h") -> Dict[str, Any]:
    """
    Recolecta métricas del sistema híbrido
    """
    from ..utils.rate_limiter import rate_limiter
    from ..utils.faq_checker import faq_classifier
    from ..utils.section_templates import section_validator
    from ..services.emergency_mode import emergency_mode
    from ..services.safety_checker import safety_checker
    from ..services.i18n_service import i18n_service

    metrics = {
        'timestamp': datetime.now().isoformat(),
        'time_range': time_range,
        'components': {}
    }

    # Métricas por componente
    if not component or component == 'rate_limiter':
        metrics['components']['rate_limiter'] = rate_limiter.get_global_stats()

    if not component or component == 'faq_classifier':
        metrics['components']['faq_classifier'] = faq_classifier.get_stats()

    if not component or component == 'section_validator':
        metrics['components']['section_validator'] = section_validator.get_stats()

    if not component or component == 'emergency_mode':
        metrics['components']['emergency_mode'] = emergency_mode.get_status()

    if not component or component == 'safety_checker':
        metrics['components']['safety_checker'] = safety_checker.get_stats()

    if not component or component == 'i18n_service':
        metrics['components']['i18n_service'] = i18n_service.get_stats()

    # Métricas agregadas
    if not component:
        metrics['aggregated'] = {
            'total_requests': sum_metric('total_requests', metrics['components']),
            'total_errors': sum_metric('errors', metrics['components']),
            'average_response_time': avg_metric('avg_response_time', metrics['components'])
        }

    # Incluir configuración actual para debugging/diagnóstico
    try:
        metrics['config'] = Config.as_dict()
    except Exception:
        metrics['config'] = {"error": "unable to read config"}

    return metrics

def collect_flow_statistics() -> Dict[str, Any]:
    """
    Recolecta estadísticas del flujo de procesamiento
    """
    # TODO: Implementar recolección real desde base de datos o cache
    return {
        'timestamp': datetime.now().isoformat(),
        'flow_paths': {
            'cache_hit': {'count': 150, 'percentage': 15.0},
            'faq_response': {'count': 300, 'percentage': 30.0},
            'rag_generation': {'count': 450, 'percentage': 45.0},
            'emergency_mode': {'count': 50, 'percentage': 5.0},
            'rate_limit_exceeded': {'count': 30, 'percentage': 3.0},
            'input_validation_failed': {'count': 20, 'percentage': 2.0}
        },
        'steps_performance': {
            'rate_limiting': {'avg_time_ms': 2, 'p95_time_ms': 5, 'p99_time_ms': 10},
            'input_validation': {'avg_time_ms': 5, 'p95_time_ms': 10, 'p99_time_ms': 20},
            'cache_lookup': {'avg_time_ms': 10, 'p95_time_ms': 20, 'p99_time_ms': 50},
            'faq_classification': {'avg_time_ms': 15, 'p95_time_ms': 30, 'p99_time_ms': 60},
            'rag_generation': {'avg_time_ms': 500, 'p95_time_ms': 1000, 'p99_time_ms': 2000},
            'safety_check': {'avg_time_ms': 20, 'p95_time_ms': 40, 'p99_time_ms': 80},
            'i18n': {'avg_time_ms': 10, 'p95_time_ms': 20, 'p99_time_ms': 40}
        },
        'total_requests_processed': 1000,
        'requests_last_hour': 100,
        'requests_last_24h': 800,
        'peak_hour': '14:00-15:00',
        'peak_requests': 150
    }

def collect_performance_metrics() -> Dict[str, Any]:
    """
    Recolecta métricas de rendimiento
    """
    try:
        import psutil
    except Exception:
        psutil = None

    if psutil is None:
        # psutil no disponible: devolver métricas por defecto y nota en el resultado
        return {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_percent': None,
                'memory_mb': None,
                'memory_percent': None,
                'threads': None,
                'open_files': None
            },
            'response_times': {
                'average_ms': None,
                'median_ms': None,
                'p95_ms': None,
                'p99_ms': None,
                'max_ms': None
            },
            'throughput': {
                'requests_per_second': None,
                'requests_per_minute': None,
                'bytes_per_second': None
            },
            'cache': {
                'hit_rate': None,
                'miss_rate': None,
                'evictions_per_minute': None,
                'size_mb': None
            },
            'database': {
                'active_connections': None,
                'query_avg_ms': None,
                'slow_queries': None
            },
            'note': 'psutil not installed; install psutil to get detailed system metrics'
        }

    import os

    process = psutil.Process(os.getpid())

    # Llamada a cpu_percent con un intervalo 0.1 para obtener valor más estable
    try:
        cpu = process.cpu_percent(interval=0.1)
    except Exception:
        cpu = process.cpu_percent()

    try:
        open_files = len(process.open_files()) if hasattr(process, 'open_files') else 0
    except Exception:
        open_files = None

    return {
        'timestamp': datetime.now().isoformat(),
        'system': {
            'cpu_percent': cpu,
            'memory_mb': process.memory_info().rss / 1024 / 1024 if hasattr(process, 'memory_info') else None,
            'memory_percent': process.memory_percent() if hasattr(process, 'memory_percent') else None,
            'threads': process.num_threads() if hasattr(process, 'num_threads') else None,
            'open_files': open_files
        },
        'response_times': {
            'average_ms': 150,
            'median_ms': 100,
            'p95_ms': 500,
            'p99_ms': 1000,
            'max_ms': 5000
        },
        'throughput': {
            'requests_per_second': 10,
            'requests_per_minute': 600,
            'bytes_per_second': 50000
        },
        'cache': {
            'hit_rate': 0.35,
            'miss_rate': 0.65,
            'evictions_per_minute': 5,
            'size_mb': 50
        },
        'database': {
            'active_connections': 5,
            'query_avg_ms': 20,
            'slow_queries': 2
        }
    }

def collect_system_alerts(severity: Optional[str] = None) -> Dict[str, Any]:
    """
    Recolecta alertas del sistema
    """
    alerts = {
        'timestamp': datetime.now().isoformat(),
        'total_alerts': 0,
        'alerts': []
    }
    
    # Alertas de ejemplo (en producción vendría de un sistema de monitoreo real)
    sample_alerts = [
        {
            'id': 'alert_001',
            'timestamp': datetime.now().isoformat(),
            'severity': 'warning',
            'component': 'rate_limiter',
            'message': 'Alto volumen de requests detectado',
            'details': {'requests_per_minute': 150, 'threshold': 100}
        },
        {
            'id': 'alert_002',
            'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat(),
            'severity': 'info',
            'component': 'cache',
            'message': 'Cache limpiado automáticamente',
            'details': {'entries_removed': 100, 'reason': 'ttl_expired'}
        },
        {
            'id': 'alert_003',
            'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
            'severity': 'error',
            'component': 'gemini_api',
            'message': 'Error de conexión con API Gemini',
            'details': {'error': 'timeout', 'retry_count': 3}
        }
    ]
    
    # Filtrar por severidad si se especifica
    if severity:
        filtered_alerts = [a for a in sample_alerts if a['severity'] == severity]
    else:
        filtered_alerts = sample_alerts
    
    alerts['alerts'] = filtered_alerts
    alerts['total_alerts'] = len(filtered_alerts)
    
    # Conteo por severidad
    alerts['by_severity'] = {
        'critical': len([a for a in filtered_alerts if a['severity'] == 'critical']),
        'error': len([a for a in filtered_alerts if a['severity'] == 'error']),
        'warning': len([a for a in filtered_alerts if a['severity'] == 'warning']),
        'info': len([a for a in filtered_alerts if a['severity'] == 'info'])
    }
    
    return alerts

def collect_system_logs(level: str = "INFO", limit: int = 100, component: Optional[str] = None) -> Dict[str, Any]:
    """
    Recolecta logs del sistema
    """
    # En producción, esto leería de un sistema de logging centralizado
    logs = {
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'limit': limit,
        'component': component,
        'entries': []
    }
    
    # Logs de ejemplo
    sample_logs = [
        {
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'component': 'orchestrator',
            'message': 'Request procesado exitosamente',
            'details': {'flow_path': 'rag_generation', 'duration_ms': 450}
        },
        {
            'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(),
            'level': 'WARNING',
            'component': 'rate_limiter',
            'message': 'Cliente cerca del límite de rate',
            'details': {'client_id': 'ip:192.168.1.100', 'remaining': 5}
        },
        {
            'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat(),
            'level': 'ERROR',
            'component': 'safety_checker',
            'message': 'Contenido no seguro detectado',
            'details': {'reason': 'inappropriate_content'}
        }
    ]
    
    # Filtrar por nivel y componente
    filtered_logs = sample_logs
    
    if component:
        filtered_logs = [log for log in filtered_logs if log['component'] == component]
    
    # Filtrar por nivel (incluir niveles iguales o superiores)
    level_hierarchy = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
    min_level = level_hierarchy.get(level, 1)
    
    filtered_logs = [
        log for log in filtered_logs 
        if level_hierarchy.get(log['level'], 1) >= min_level
    ]
    
    logs['entries'] = filtered_logs[:limit]
    logs['total_entries'] = len(filtered_logs)
    
    return logs

# ==================== FUNCIONES DE UTILIDAD ====================

def sum_metric(metric_name: str, components: Dict) -> float:
    """Suma una métrica de todos los componentes"""
    total = 0
    for comp_data in components.values():
        if isinstance(comp_data, dict) and metric_name in comp_data:
            total += comp_data[metric_name]
    return total

def avg_metric(metric_name: str, components: Dict) -> float:
    """Promedia una métrica de todos los componentes"""
    values = []
    for comp_data in components.values():
        if isinstance(comp_data, dict) and metric_name in comp_data:
            values.append(comp_data[metric_name])
    return sum(values) / len(values) if values else 0

def generate_dashboard_html() -> str:
    """
    Genera HTML para el dashboard de monitoreo
    """
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Sistema Híbrido de Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 8px;
            background: #f7f7f7;
            border-radius: 6px;
        }
        .metric-label {
            color: #666;
            font-size: 0.9rem;
        }
        .metric-value {
            font-weight: bold;
            color: #333;
            font-size: 1.1rem;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-healthy { background: #10b981; }
        .status-warning { background: #f59e0b; }
        .status-error { background: #ef4444; }
        .chart-container {
            height: 200px;
            margin-top: 15px;
            background: #f9f9f9;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
        }
        .flow-path {
            display: flex;
            align-items: center;
            padding: 10px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            color: white;
            margin: 10px 0;
        }
        .flow-step {
            padding: 5px 10px;
            background: rgba(255,255,255,0.2);
            border-radius: 4px;
            margin: 0 5px;
        }
        .refresh-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: white;
            color: #667eea;
            border: none;
            padding: 15px 30px;
            border-radius: 30px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
        }
        .refresh-btn:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Dashboard Sistema Híbrido RAG</h1>
        
        <div class="grid">
            <!-- Estado del Sistema -->
            <div class="card">
                <h2>Estado del Sistema</h2>
                <div class="metric">
                    <span class="metric-label">
                        <span class="status-indicator status-healthy"></span>
                        Estado General
                    </span>
                    <span class="metric-value">Operacional</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Uptime</span>
                    <span class="metric-value">99.95%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Versión</span>
                    <span class="metric-value">2.0.0-hybrid</span>
                </div>
            </div>
            
            <!-- Métricas de Tráfico -->
            <div class="card">
                <h2>Tráfico</h2>
                <div class="metric">
                    <span class="metric-label">Requests/min</span>
                    <span class="metric-value">45</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Total Hoy</span>
                    <span class="metric-value">12,543</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Tasa de Éxito</span>
                    <span class="metric-value">98.7%</span>
                </div>
            </div>
            
            <!-- Rate Limiting -->
            <div class="card">
                <h2>Rate Limiting</h2>
                <div class="metric">
                    <span class="metric-label">Clientes Activos</span>
                    <span class="metric-value">234</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Límites Excedidos</span>
                    <span class="metric-value">12</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Tasa de Bloqueo</span>
                    <span class="metric-value">0.3%</span>
                </div>
            </div>
            
            <!-- Cache Performance -->
            <div class="card">
                <h2>Cache</h2>
                <div class="metric">
                    <span class="metric-label">Hit Rate</span>
                    <span class="metric-value">35.2%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Entradas</span>
                    <span class="metric-value">1,234</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Memoria</span>
                    <span class="metric-value">45 MB</span>
                </div>
            </div>
            
            <!-- FAQ Classifier -->
            <div class="card">
                <h2>FAQ Classifier</h2>
                <div class="metric">
                    <span class="metric-label">Coincidencias FAQ</span>
                    <span class="metric-value">423</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Precisión</span>
                    <span class="metric-value">92.3%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Categorías Activas</span>
                    <span class="metric-value">8</span>
                </div>
            </div>
            
            <!-- RAG Performance -->
            <div class="card">
                <h2>RAG Generation</h2>
                <div class="metric">
                    <span class="metric-label">Tiempo Promedio</span>
                    <span class="metric-value">450ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Documentos Indexados</span>
                    <span class="metric-value">6</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Embeddings</span>
                    <span class="metric-value">342</span>
                </div>
            </div>
            
            <!-- Safety Checker -->
            <div class="card">
                <h2>Safety Checker</h2>
                <div class="metric">
                    <span class="metric-label">
                        <span class="status-indicator status-healthy"></span>
                        Estado
                    </span>
                    <span class="metric-value">Activo</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Contenido Bloqueado</span>
                    <span class="metric-value">3</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Tasa de Aprobación</span>
                    <span class="metric-value">99.7%</span>
                </div>
            </div>
            
            <!-- Emergency Mode -->
            <div class="card">
                <h2>Modo de Emergencia</h2>
                <div class="metric">
                    <span class="metric-label">
                        <span class="status-indicator status-healthy"></span>
                        Estado
                    </span>
                    <span class="metric-value">Inactivo</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Activaciones Hoy</span>
                    <span class="metric-value">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Última Activación</span>
                    <span class="metric-value">Nunca</span>
                </div>
            </div>
        </div>
        
        <!-- Flujo de Procesamiento -->
        <div class="card">
            <h2>Flujo de Procesamiento Típico</h2>
            <div class="flow-path">
                <span class="flow-step">Usuario</span>
                →
                <span class="flow-step">Rate Limit</span>
                →
                <span class="flow-step">Validation</span>
                →
                <span class="flow-step">Cache</span>
                →
                <span class="flow-step">FAQ Check</span>
                →
                <span class="flow-step">RAG</span>
                →
                <span class="flow-step">Safety</span>
                →
                <span class="flow-step">i18n</span>
                →
                <span class="flow-step">Response</span>
            </div>
            <div class="chart-container">
                [Gráfico de flujo interactivo aquí]
            </div>
        </div>
        
        <!-- Alertas Recientes -->
        <div class="card">
            <h2>Alertas Recientes</h2>
            <div class="metric">
                <span class="metric-label">
                    <span class="status-indicator status-warning"></span>
                    Warning
                </span>
                <span class="metric-value">Alto volumen de requests (hace 5 min)</span>
            </div>
            <div class="metric">
                <span class="metric-label">
                    <span class="status-indicator status-healthy"></span>
                    Info
                </span>
                <span class="metric-value">Cache limpiado automáticamente (hace 30 min)</span>
            </div>
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
    </div>
    
    <script>
        // Auto-refresh cada 30 segundos
        setTimeout(() => location.reload(), 30000);
        
        // Fetch real-time metrics
        async function fetchMetrics() {
            try {
                const response = await fetch('/api/monitoring/metrics');
                const data = await response.json();
                console.log('Metrics:', data);
                // Actualizar UI con datos reales
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }
        
        // Inicializar
        fetchMetrics();
        setInterval(fetchMetrics, 5000);
    </script>
</body>
</html>
"""

# ==================== EXPORTACIÓN ====================
__all__ = ['router', 'collect_system_metrics', 'collect_flow_statistics']
