// 📡 ChatServicio.js - Puente entre Frontend y Backend
// Conecta tu React con tu backend FastAPI

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class ChatService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.timeout = 30000; // 30 segundos máximo
  }

  /**
   * 📤 FUNCIÓN PRINCIPAL: Envía mensaje al backend
   * @param {string} message - Lo que escribió el usuario
   * @param {string} section - Sección actual (sobreheily, proyectos, etc)
   * @param {AbortSignal} signal - Para cancelar request si es necesario
   * @returns {Promise<Object>} - Respuesta del backend
   */
  async sendMessage(message, section = 'sobreheily', signal = null) {
    try {
      // 🎯 PASO 1: Validar que tenemos los datos básicos
      if (!message || !message.trim()) {
        throw new Error('El mensaje no puede estar vacío');
      }

      // ⏰ PASO 2: Setup de timeout automático
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      // 🔄 PASO 3: Usar signal externo si existe, sino el interno
      const finalSignal = signal || controller.signal;

      // 📦 PASO 4: Preparar datos para enviar (compatible con tu backend actual)
      const requestData = {
        message: message.trim(),
        section: section,
        context: null, // Tu backend acepta context opcional
        timestamp: Date.now()
      };

      console.log('🚀 Enviando al backend:', requestData);

      // 📡 PASO 5: Hacer la llamada a tu backend actual
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        signal: finalSignal
      });

      // 🧹 PASO 6: Limpiar timeout
      clearTimeout(timeoutId);

      // ❌ PASO 7: Manejar errores HTTP específicos
      if (!response.ok) {
        switch (response.status) {
          case 400:
            throw new Error('Mensaje inválido. Por favor reformula tu pregunta.');
          case 429:
            throw new Error('Demasiadas solicitudes. Espera un momento e intenta de nuevo.');
          case 500:
            throw new Error('Error del servidor. Intenta de nuevo más tarde.');
          case 503:
            throw new Error('Servicio no disponible. Intenta más tarde.');
          default:
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
      }

      // 📋 PASO 8: Convertir respuesta a JSON
      const data = await response.json();
      
      console.log('✅ Respuesta del backend:', data);

      // 🔍 PASO 9: Validar que la respuesta tiene lo que esperamos
      if (!data.response) {
        throw new Error('Respuesta inválida del servidor');
      }

      // 🎉 PASO 10: Retornar respuesta limpia para el frontend
      return {
        response: data.response,
        metadata: data.metadata || {},
        error: data.error || null,
        timestamp: Date.now()
      };

    } catch (error) {
      // 🛑 MANEJO DE ERRORES ESPECIALES

      // Si se canceló el request
      if (error.name === 'AbortError') {
        console.log('⏹️ Request cancelado por el usuario');
        throw error;
      }

      console.error('❌ Error en ChatService:', error);

      // 🌐 Errores de red (sin internet, backend caído, etc)
      if (error.message.includes('Failed to fetch') || 
          error.message.includes('NetworkError') ||
          error.message.includes('Type error')) {
        throw new Error('Error de conexión. Verifica tu internet e intenta de nuevo.');
      }

      // ⏰ Timeout
      if (error.message.includes('timeout')) {
        throw new Error('La respuesta está tardando mucho. Intenta de nuevo.');
      }

      // 🔄 Re-throw otros errores tal como están
      throw error;
    }
  }

  /**
   * 🏥 FUNCIÓN AUXILIAR: Verificar estado del sistema 
   * Esta función es útil para saber si el backend está funcionando correctamente
   * y si la API está accesible antes de enviar mensajes.
   * Puedes usarla para mostrar un mensaje de estado en la UI o para hacer un health check inicial.
   * 💡 Úsala al inicio de la app o cuando el usuario lo solicite.
   */
  async getSystemStatus() {
    try {
      const response = await fetch(`${this.baseURL}/chat/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Status check failed: ${response.status}`);
      }

      return await response.json();

    } catch (error) {
      console.error('❌ Status check error:', error);
      return { error: error.message, healthy: false };
    }
  }

  /**
   * 💓 FUNCIÓN AUXILIAR: Health check rápido
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET'
      });

      return response.ok;

    } catch (error) {
      console.error('❌ Health check failed:', error);
      return false;
    }
  }
}

// 🏭 EXPORTAR INSTANCIA ÚNICA (Singleton)
// Toda la app usa la misma instancia del servicio
export default new ChatService();
