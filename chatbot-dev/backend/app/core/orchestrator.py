import logging
import hashlib
import json
from typing import Dict, Any, List, Optional
from ..interfaces import ILLMProvider, IEmbeddingProvider, IVectorStore, IDocumentProcessor, ICacheProvider
from .factory import ProviderFactory
from ..config.settings import Config

# Importar componentes del diagrama híbrido
from ..utils.rate_limiter import check_rate_limit, get_client_identifier
from ..utils.sanitizer import process_user_input
from ..utils.faq_checker import classify_user_message
from ..utils.section_templates import validate_message_section
from ..services.emergency_mode import emergency_mode, handle_emergency, check_emergency_activation
from ..services.safety_checker import check_input_safety, check_output_safety
from ..services.i18n_service import translate_response, detect_user_language

logger = logging.getLogger(__name__)

class HybridRAGOrchestrator:
    """
    Orquestador RAG Híbrido según diagrama de flujo completo
    Implementa: Rate Limiting -> Validation -> Processing -> Cache -> Health Check -> 
               Section Validation -> FAQ -> RAG -> Safety -> i18n -> Response
    """
    
    def __init__(self, provider_config: Dict[str, str] = None):
        """Inicializa el orquestador híbrido"""
        
        # Crear proveedores usando factory
        self.providers = ProviderFactory.create_all_providers(provider_config)
        
        # Extraer proveedores para fácil acceso
        self.llm_provider: ILLMProvider = self.providers['llm']
        self.embedding_provider: IEmbeddingProvider = self.providers['embedding']
        self.vector_store: IVectorStore = self.providers['vector_store']
        self.document_processor: IDocumentProcessor = self.providers['document_processor']
        self.cache_provider: ICacheProvider = self.providers['cache']
        
        # Estado de inicialización
        self.is_initialized = False
        self.initialization_error = None
        
        # Inicializar documentos
        self._initialize_documents()
        
        logger.info("HybridRAGOrchestrator inicializado con flujo completo")
    
    def process_hybrid_request(self, message: str, client_identifier: str, user_context: Optional[str] = None, target_language: str = "es") -> Dict[str, Any]:
        """
        Procesa request completa según diagrama híbrido
        
        Args:
            message: Mensaje del usuario
            client_identifier: Identificador del cliente (IP, user ID)
            user_context: Contexto adicional opcional
            target_language: Idioma objetivo para respuesta
        
        Returns:
            Dict con respuesta procesada según flujo híbrido
        """
        flow_metadata = {
            'steps_completed': [],
            'processing_time': {},
            'flow_path': []
        }
        
        try:
            import time
            start_time = time.time()
            
            # PASO 1: RATE LIMITING
            step_start = time.time()
            rate_result = check_rate_limit(client_identifier, "chat")
            flow_metadata['steps_completed'].append('rate_limiting')
            flow_metadata['processing_time']['rate_limiting'] = time.time() - step_start
            
            if not rate_result.get('allowed', False):
                flow_metadata['flow_path'].append('rate_limit_exceeded')
                return self._create_response(
                    success=False,
                    response=self._get_localized_message('rate_limit_exceeded', target_language),
                    error="Rate limit exceeded",
                    metadata=flow_metadata,
                    retry_after=rate_result.get('retry_after', 60)
                )
            
            # PASO 2: VALIDACIÓN DE ENTRADA
            step_start = time.time()
            input_validation = process_user_input(message, user_context)
            flow_metadata['steps_completed'].append('input_validation')
            flow_metadata['processing_time']['input_validation'] = time.time() - step_start
            
            if not input_validation.get('is_valid', False):
                flow_metadata['flow_path'].append('input_validation_failed')
                return self._create_response(
                    success=False,
                    response=self._get_localized_message('input_too_long', target_language),
                    error="Input validation failed",
                    metadata=flow_metadata,
                    validation_issues=input_validation.get('warnings', [])
                )
            
            # Usar mensaje procesado
            processed_message = input_validation['processed_message']
            flow_metadata['input_transformations'] = input_validation.get('transformations', [])
            
            # PASO 3: VERIFICACIÓN DE SEGURIDAD DE ENTRADA
            step_start = time.time()
            input_safety = check_input_safety(processed_message)
            flow_metadata['steps_completed'].append('input_safety')
            flow_metadata['processing_time']['input_safety'] = time.time() - step_start
            
            if not input_safety.get('is_safe', True):
                flow_metadata['flow_path'].append('input_unsafe')
                return self._create_response(
                    success=False,
                    response=self._get_localized_message('inappropriate_content', target_language),
                    error="Unsafe input detected",
                    metadata=flow_metadata,
                    safety_issues=input_safety.get('issues', [])
                )
            
            # PASO 4: CACHE LOOKUP
            step_start = time.time()
            cache_key = self._generate_cache_key(processed_message, user_context, target_language)
            cached_response = None

            if self.cache_provider:
                cached_response = self.cache_provider.get(cache_key)

            flow_metadata['steps_completed'].append('cache_lookup')
            flow_metadata['processing_time']['cache_lookup'] = time.time() - step_start

            # Intentar instrumentación Prometheus (import seguro)
            try:
                from ..monitoring.prometheus_exporter import inc_cache_hit, inc_request, inc_error, observe_response_time
            except Exception:
                inc_cache_hit = None
                inc_request = None
                inc_error = None
                observe_response_time = None

            if cached_response:
                flow_metadata['flow_path'].append('cache_hit')
                cached_response['from_cache'] = True
                cached_response['metadata'].update(flow_metadata)
                # Instrumentar cache hit
                try:
                    if inc_cache_hit:
                        inc_cache_hit(endpoint='cache_lookup')
                except Exception:
                    pass
                return cached_response

            flow_metadata['flow_path'].append('cache_miss')
            
            # PASO 5: HEALTH CHECK DE SERVICIOS
            step_start = time.time()
            services_health = self._check_services_health()
            flow_metadata['steps_completed'].append('health_check')
            flow_metadata['processing_time']['health_check'] = time.time() - step_start
            flow_metadata['services_status'] = services_health
            
            # PASO 6: VERIFICAR SI ACTIVAR MODO DE EMERGENCIA
            emergency_activated = check_emergency_activation(
                services_health['llm_available'],
                services_health['vector_store_available'],
                services_health['embedding_available']
            )
            
            if not emergency_activated and emergency_mode.is_active:
                flow_metadata['flow_path'].append('emergency_mode')
                step_start = time.time()
                emergency_response = handle_emergency(processed_message)
                flow_metadata['processing_time']['emergency_mode'] = time.time() - step_start
                
                # Traducir respuesta de emergencia
                translated_response = translate_response(emergency_response, target_language)
                translated_response['metadata'] = flow_metadata
                return translated_response
            
            # PASO 7: VALIDACIÓN DE SECCIÓN
            step_start = time.time()
            section_validation = validate_message_section(processed_message)
            flow_metadata['steps_completed'].append('section_validation')
            flow_metadata['processing_time']['section_validation'] = time.time() - step_start
            flow_metadata['detected_section'] = section_validation.get('detected_section', 'general')
            
            if not section_validation.get('is_valid', True):
                enforcement_action = section_validation.get('enforcement_action', 'proceed')
                
                if enforcement_action == 'guide':
                    flow_metadata['flow_path'].append('section_guidance')
                    return self._create_response(
                        success=True,
                        response=section_validation.get('guidance', ''),
                        guidance=True,
                        metadata=flow_metadata,
                        question_templates=section_validation.get('question_templates', [])
                    )
                elif enforcement_action == 'clarify':
                    flow_metadata['flow_path'].append('section_clarification')
                    return self._create_response(
                        success=True,
                        response=section_validation.get('guidance', ''),
                        clarification_needed=True,
                        metadata=flow_metadata,
                        conflicting_sections=section_validation.get('conflicting_sections', [])
                    )
            
            # PASO 8: CLASIFICACIÓN FAQ
            step_start = time.time()
            faq_classification = classify_user_message(processed_message)
            flow_metadata['steps_completed'].append('faq_classification')
            flow_metadata['processing_time']['faq_classification'] = time.time() - step_start
            
            if faq_classification.get('is_faq', False) and faq_classification.get('confidence', 0) > 0.7:
                flow_metadata['flow_path'].append('faq_response')
                faq_response = self._create_response(
                    success=True,
                    response=faq_classification['response'],
                    source='faq',
                    confidence=faq_classification['confidence'],
                    category=faq_classification.get('category', 'general'),
                    metadata=flow_metadata
                )
                
                # Cache y traducir respuesta FAQ
                translated_response = translate_response(faq_response, target_language)
                self._cache_response(cache_key, translated_response)
                return translated_response
            
            # PASO 9: BÚSQUEDA RAG + GENERACIÓN LLM
            flow_metadata['flow_path'].append('rag_generation')
            
            # Verificar disponibilidad de Gemini Free Tier
            if not services_health['llm_available']:
                flow_metadata['flow_path'].append('llm_unavailable_template')
                template_response = self._get_template_response("llm_unavailable", target_language)
                template_response['metadata'] = flow_metadata
                return template_response
            
            # Generar respuesta usando RAG
            step_start = time.time()
            rag_response = self._generate_rag_response(processed_message, user_context)
            flow_metadata['processing_time']['rag_generation'] = time.time() - step_start

            # Instrumentar latencia de generación RAG
            try:
                if observe_response_time and flow_metadata.get('processing_time', {}).get('rag_generation'):
                    observe_response_time(endpoint='rag_generation', seconds=flow_metadata['processing_time']['rag_generation'])
            except Exception:
                pass

            if not rag_response.get('success', False):
                flow_metadata['flow_path'].append('rag_error_template')
                # Instrumentar error
                try:
                    if inc_error:
                        inc_error(endpoint='rag_generation', err_type='generation_error')
                except Exception:
                    pass
                template_response = self._get_template_response("generation_error", target_language)
                template_response['metadata'] = flow_metadata
                return template_response
            
            # PASO 10: SAFETY CHECK DE RESPUESTA
            step_start = time.time()
            safety_context = {
                'user_message': processed_message,
                'detected_section': section_validation.get('detected_section')
            }
            output_safety = check_output_safety(rag_response['response'], safety_context)
            flow_metadata['steps_completed'].append('output_safety')
            flow_metadata['processing_time']['output_safety'] = time.time() - step_start
            
            if not output_safety.get('is_safe', True):
                flow_metadata['flow_path'].append('output_unsafe_template')
                template_response = self._get_template_response("unsafe_output", target_language)
                template_response['metadata'] = flow_metadata
                template_response['safety_issues'] = output_safety.get('issues', [])
                return template_response
            
            # Usar respuesta segura
            final_response_text = output_safety.get('safe_response', rag_response['response'])
            
            # PASO 11: ESTRUCTURAR RESPUESTA
            structured_response = self._create_response(
                success=True,
                response=final_response_text,
                source='rag',
                sources_used=rag_response.get('sources_used', 0),
                context_found=rag_response.get('context_found', False),
                model_info=rag_response.get('model_info', {}),
                metadata=flow_metadata,
                safety_passed=True
            )
            
            # PASO 12: INTERNACIONALIZACIÓN
            step_start = time.time()
            translated_response = translate_response(structured_response, target_language)
            flow_metadata['processing_time']['i18n'] = time.time() - step_start
            flow_metadata['steps_completed'].append('i18n')
            
            # PASO 13: CACHE Y RETORNO
            translated_response['metadata'] = flow_metadata
            translated_response['total_processing_time'] = time.time() - start_time
            self._cache_response(cache_key, translated_response)
            # Instrumentar cache set (no inc_cache_hit, pero podría incrementarse en cache provider)
            try:
                if inc_request:
                    inc_request(endpoint='chat', method='POST')
            except Exception:
                pass

            return translated_response
            
        except Exception as e:
            logger.error(f"Error en flujo híbrido: {e}")
            flow_metadata['flow_path'].append('critical_error')
            return self._create_response(
                success=False,
                response=self._get_localized_message('system_error', target_language),
                error=str(e),
                metadata=flow_metadata
            )
    
    def _initialize_documents(self):
        """Inicializa documentos en el sistema (heredado del orquestador original)"""
        try:
            if not self.document_processor or not self.embedding_provider or not self.vector_store:
                self.initialization_error = "Proveedores críticos no disponibles"
                return
            
            documents = self.document_processor.load_documents()
            if not documents:
                logger.warning("No se encontraron documentos para cargar")
                self.is_initialized = True
                return
            
            embeddings = []
            for doc in documents:
                embedding = self.embedding_provider.generate_embedding(doc['content'])
                if embedding:
                    embeddings.append(embedding)
                else:
                    logger.warning(f"No se pudo generar embedding para: {doc.get('metadata', {}).get('filename', 'unknown')}")
            
            valid_documents = [doc for doc, emb in zip(documents, embeddings) if emb]
            valid_embeddings = [emb for emb in embeddings if emb]
            
            if valid_documents:
                success = self.vector_store.add_documents(valid_documents, valid_embeddings)
                if success:
                    logger.info(f"Inicializados {len(valid_documents)} documentos en RAG")
                    self.is_initialized = True
                else:
                    self.initialization_error = "Error agregando documentos al vector store"
            else:
                self.initialization_error = "No se pudieron procesar embeddings"
                
        except Exception as e:
            logger.error(f"Error inicializando documentos: {e}")
            self.initialization_error = str(e)
    
    def _check_services_health(self) -> Dict[str, bool]:
        """Verifica salud de todos los servicios"""
        return {
            'llm_available': self.llm_provider and self.llm_provider.is_available(),
            'embedding_available': self.embedding_provider and self.embedding_provider.is_available(),
            'vector_store_available': self.vector_store and getattr(self.vector_store, 'is_available', lambda: True)(),
            'cache_available': self.cache_provider is not None,
            'documents_initialized': self.is_initialized
        }
    
    def _generate_rag_response(self, message: str, user_context: Optional[str] = None) -> Dict[str, Any]:
        """Genera respuesta usando RAG (heredado y mejorado)"""
        try:
            relevant_context = self._search_relevant_context(message)
            enhanced_prompt = self._build_enhanced_prompt(message, relevant_context, user_context)
            llm_response = self.llm_provider.generate_response(enhanced_prompt)
            
            return {
                'success': llm_response.get('success', False),
                'response': llm_response.get('response', ''),
                'sources_used': len(relevant_context),
                'context_found': bool(relevant_context),
                'model_info': self.llm_provider.get_model_info()
            }
        except Exception as e:
            logger.error(f"Error en generación RAG: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _search_relevant_context(self, message: str) -> List[Dict]:
        """Busca contexto relevante (heredado)"""
        try:
            if not self.embedding_provider or not self.vector_store or not self.is_initialized:
                return []
            
            query_embedding = self.embedding_provider.generate_embedding(message)
            if not query_embedding:
                return []
            
            similar_docs = self.vector_store.search_similar(query_embedding, Config.SIMILARITY_TOP_K)
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error buscando contexto: {e}")
            return []
    
    def _build_enhanced_prompt(self, message: str, relevant_context: List[Dict], user_context: Optional[str] = None) -> str:
        """Construye prompt enriquecido (heredado)"""
        system_context = """Eres un asistente AI especializado en ayudar con consultas sobre mi perfil profesional y portfolio.

Tu personalidad:
- Profesional pero amigable
- Conocedor de mi experiencia y habilidades  
- Capaz de explicar proyectos técnicos de manera clara
- Entusiasta sobre tecnología y desarrollo

Tipos de consultas que puedes manejar:
- Información sobre mi experiencia profesional
- Detalles de proyectos desarrollados
- Habilidades técnicas y tecnologías
- Formación académica y certificaciones
- Información de contacto
- Disponibilidad para oportunidades laborales"""
        
        documents_context = ""
        if relevant_context:
            documents_context = "\n\nINFORMACIÓN RELEVANTE DE MIS DOCUMENTOS:\n"
            for i, doc in enumerate(relevant_context, 1):
                content = doc['content'][:500] + "..." if len(doc['content']) > 500 else doc['content']
                documents_context += f"\n[Fuente {i}]: {content}"
                
                filename = doc.get('metadata', {}).get('filename')
                if filename:
                    documents_context += f" (de: {filename})"
        
        user_info = ""
        if user_context:
            user_info = f"\n\nCONTEXTO DEL USUARIO: {user_context}"
        
        prompt = f"""{system_context}
        
{documents_context}
{user_info}

CONSULTA DEL USUARIO: {message}

INSTRUCCIONES:
- Responde de manera profesional y amigable
- Usa SOLO la información de mis documentos cuando sea relevante
- Si no tienes información específica, sé honesto al respecto
- Mantén un tono conversacional pero profesional
- Si mencionas información de mis documentos, puedes hacer referencia general a ellos
- Adapta la respuesta al contexto de la consulta

RESPUESTA:"""
        
        return prompt
    
    def _create_response(self, success: bool, response: str, **kwargs) -> Dict[str, Any]:
        """Crea respuesta estructurada"""
        base_response = {
            'success': success,
            'response': response,
            'timestamp': __import__('time').time(),
            'from_cache': False
        }
        base_response.update(kwargs)
        return base_response
    
    def _get_template_response(self, template_type: str, language: str = "es") -> Dict[str, Any]:
        """Obtiene respuesta de template según el tipo"""
        templates = {
            "llm_unavailable": {
                "es": "Los servicios de IA no están disponibles temporalmente. Por favor intenta más tarde.",
                "en": "AI services are temporarily unavailable. Please try again later."
            },
            "generation_error": {
                "es": "Hubo un error generando la respuesta. Por favor intenta de nuevo.",
                "en": "There was an error generating the response. Please try again."
            },
            "unsafe_output": {
                "es": "La respuesta generada no pasó los filtros de seguridad. Por favor reformula tu pregunta.",
                "en": "The generated response did not pass safety filters. Please rephrase your question."
            }
        }
        
        template_text = templates.get(template_type, {}).get(language, 
                                                           templates.get(template_type, {}).get("es", 
                                                                                               "Error del sistema"))
        
        return self._create_response(
            success=False,
            response=template_text,
            source='template',
            template_type=template_type
        )
    
    def _get_localized_message(self, key: str, language: str) -> str:
        """Obtiene mensaje localizado"""
        from ..services.i18n_service import get_localized_message
        return get_localized_message(key, language)
    
    def _generate_cache_key(self, message: str, user_context: Optional[str] = None, language: str = "es") -> str:
        """Genera clave de cache incluyendo idioma"""
        content = f"{message}_{user_context or ''}_{language}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cache_response(self, cache_key: str, response: Dict[str, Any]):
        """Guarda respuesta en cache"""
        try:
            if self.cache_provider:
                # Remover metadata temporal antes de cachear
                cached_response = response.copy()
                if 'metadata' in cached_response:
                    cached_response['metadata'] = {
                        k: v for k, v in cached_response['metadata'].items() 
                        if k in ['steps_completed', 'flow_path', 'detected_section']
                    }
                self.cache_provider.set(cache_key, cached_response, ttl=3600)
                # Instrumentar cache set (si está disponible)
                try:
                    from ..monitoring.prometheus_exporter import inc_request
                    if inc_request:
                        inc_request(endpoint='cache_set', method='SET')
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Error cacheando respuesta: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Estado completo del sistema híbrido"""
        try:
            base_status = {
                'initialized': self.is_initialized,
                'initialization_error': self.initialization_error,
                'providers': {},
                'hybrid_components': {}
            }
            
            # Estado de proveedores base
            provider_names = ['llm', 'embedding', 'vector_store', 'document_processor', 'cache']
            for name in provider_names:
                provider = self.providers.get(name)
                if provider:
                    base_status['providers'][name] = {
                        'available': getattr(provider, 'is_available', lambda: True)(),
                        'type': provider.__class__.__name__
                    }
                else:
                    base_status['providers'][name] = {
                        'available': False,
                        'type': 'None'
                    }
            
            # Estado de componentes híbridos
            from ..utils.rate_limiter import rate_limiter
            from ..utils.faq_checker import faq_classifier
            from ..utils.section_templates import section_validator
            from ..services.safety_checker import safety_checker
            from ..services.i18n_service import i18n_service
            
            base_status['hybrid_components'] = {
                'rate_limiter': rate_limiter.get_global_stats(),
                'faq_classifier': faq_classifier.get_stats(),
                'section_validator': section_validator.get_stats(),
                'emergency_mode': emergency_mode.get_status(),
                'safety_checker': safety_checker.get_stats(),
                'i18n_service': i18n_service.get_stats()
            }
            
            # Stats adicionales
            if self.vector_store:
                base_status['vector_store_stats'] = self.vector_store.get_stats()
            
            if self.document_processor:
                base_status['documents_info'] = self.document_processor.get_documents_info()
            
            return base_status
            
        except Exception as e:
            logger.error(f"Error obteniendo estado del sistema: {e}")
            return {"error": str(e)}

    def reload_documents(self) -> Dict[str, Any]:
        """Recarga documentos con limpieza de componentes"""
        try:
            logger.info("Recargando documentos en sistema híbrido...")
            
            # Limpiar vector store
            if self.vector_store:
                self.vector_store.clear()
            
            # Limpiar cache
            if self.cache_provider:
                self.cache_provider.clear()
            
            # Reinicializar
            self.is_initialized = False
            self.initialization_error = None
            self._initialize_documents()
            
            if self.is_initialized:
                return {"success": True, "message": "Documentos recargados exitosamente en sistema híbrido"}
            else:
                return {"success": False, "error": self.initialization_error}
                
        except Exception as e:
            logger.error(f"Error recargando documentos: {e}")
            return {"success": False, "error": str(e)}

# Alias para compatibilidad
RAGOrchestrator = HybridRAGOrchestrator
