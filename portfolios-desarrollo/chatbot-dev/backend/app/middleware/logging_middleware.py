"""
Middleware de logging estructurado y mascaramiento de PII
Soporta FastAPI (middleware) y Flask (registro before/after)
"""
import logging
import json
import re
from typing import Callable
from fastapi import Request

logger = logging.getLogger("structured_logger")

# Patrones PII comunes
_EMAIL_RE = re.compile(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
_SSN_RE = re.compile(r"\b(\d{3}[- ]?\d{2}[- ]?\d{4})\b")
_CC_RE = re.compile(r"\b(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})\b")
_PHONE_RE = re.compile(r"\b(\+?\d{1,3}[\s-]?)?(\(?\d{2,4}\)?[\s-]?)?\d{6,10}\b")


def _mask_email(match: re.Match) -> str:
    user = match.group(1)
    domain = match.group(2)
    masked_user = user[0] + "***" + user[-1] if len(user) > 2 else "***"
    return f"{masked_user}@{domain}"


def _mask_generic(match: re.Match) -> str:
    s = match.group(0)
    if len(s) <= 4:
        return "[PII]"
    return s[:2] + "*" * (len(s) - 4) + s[-2:]


def mask_pii(text: str) -> str:
    if not text:
        return text
    try:
        text = _EMAIL_RE.sub(_mask_email, text)
        text = _SSN_RE.sub(lambda m: _mask_generic(m), text)
        text = _CC_RE.sub(lambda m: _mask_generic(m), text)
        text = _PHONE_RE.sub(lambda m: _mask_generic(m), text)
        return text
    except Exception:
        return text


class StructuredLoggingMiddleware:
    """Middleware ligero para FastAPI que genera logs JSON y mascara PII"""
    def __init__(self, app, log_level: int = logging.INFO):
        self.app = app
        self.log_level = log_level
        self.logger = logging.getLogger("structured_logger")
        self.logger.setLevel(log_level)

    async def __call__(self, request: Request, call_next: Callable):
        # Log entrada estructurada
        try:
            payload_preview = None
            try:
                payload = await request.body()
                payload_preview = payload.decode('utf-8', errors='ignore')[:1000]
            except Exception:
                payload_preview = None

            headers = {k.decode('latin1'): v.decode('latin1') for k, v in request.scope.get('headers', [])}
            # Mask headers that may contain PII or auth
            if 'authorization' in headers:
                headers['authorization'] = 'REDACTED'
            if 'x-api-key' in headers:
                headers['x-api-key'] = 'REDACTED'

            log_entry = {
                'event': 'request_received',
                'method': request.method,
                'path': request.url.path,
                'client': request.client.host if request.client else None,
                'headers': headers,
                'payload_preview': mask_pii(payload_preview) if payload_preview else None
            }
            self.logger.info(json.dumps(log_entry))
        except Exception:
            pass

        # Llamar al siguiente handler
        response = await call_next(request)

        # Log respuesta
        try:
            response_log = {
                'event': 'response_sent',
                'method': request.method,
                'path': request.url.path,
                'status_code': getattr(response, 'status_code', None)
            }
            self.logger.info(json.dumps(response_log))
        except Exception:
            pass

        return response


# Funciones para Flask
def register_flask_logging(app):
    """Registra handlers before_request y after_request para flask"""
    try:
        from flask import request
        import time
        from flask import g

        # Intentar importar helpers de prometheus de forma segura
        try:
            from ..monitoring.prometheus_exporter import inc_request, observe_response_time, inc_error
        except Exception:
            inc_request = None
            observe_response_time = None
            inc_error = None

        @app.before_request
        def _before():
            try:
                # Instrumentación: marcar inicio para medir latencia
                try:
                    g._start_time = time.time()
                except Exception:
                    g._start_time = None

                # Incrementar contador de requests Prometheus si está disponible
                try:
                    if inc_request:
                        endpoint = request.path or 'unknown'
                        method = request.method or 'GET'
                        inc_request(endpoint=endpoint, method=method)
                except Exception:
                    pass

                payload = None
                try:
                    payload = request.get_data(as_text=True)[:1000]
                except Exception:
                    payload = None

                headers = {k: v for k, v in request.headers.items()}
                if 'Authorization' in headers:
                    headers['Authorization'] = 'REDACTED'
                if 'X-API-Key' in headers:
                    headers['X-API-Key'] = 'REDACTED'

                log_entry = {
                    'event': 'request_received',
                    'method': request.method,
                    'path': request.path,
                    'client': request.remote_addr,
                    'headers': headers,
                    'payload_preview': mask_pii(payload) if payload else None
                }
                logger.info(json.dumps(log_entry))
            except Exception:
                pass

        @app.after_request
        def _after(response):
            try:
                # Medir latencia y enviar a Prometheus si está disponible
                try:
                    if getattr(g, '_start_time', None):
                        duration = time.time() - g._start_time
                        if observe_response_time:
                            endpoint = request.path or 'unknown'
                            observe_response_time(endpoint=endpoint, seconds=duration)
                except Exception:
                    pass

                response_log = {
                    'event': 'response_sent',
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code
                }
                logger.info(json.dumps(response_log))
            except Exception:
                pass
            return response

        # Registrar handler de errores para contar errores en Prometheus
        @app.register_error_handler(Exception)
        def _handle_exception(error):
            try:
                if inc_error:
                    endpoint = request.path if request else 'unknown'
                    inc_error(endpoint=endpoint, err_type=type(error).__name__)
            except Exception:
                pass
            # Re-lanzar el error para que Flask lo maneje normalmente
            raise error

        logger.info('Flask structured logging registered')
    except Exception as e:
        logger.warning(f'Could not register Flask logging: {e}')
