import React, { useState } from 'react';
import './MessageInput.css';
import chatService from '../../../services/chat/chatServicio'; // Servicio de chat

const MessageInput = ({ language, onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      setIsLoading(true);

      try {
        // 📤 Llamar al servicio (ahora incluye modo emergencia automático)
        const response = await chatService.sendMessage(
          message.trim(),
          'sobreheily' // Cambia según la sección que necesites
        );

        console.log('✅ Bot respondió:', response.response);
        console.log('📊 Metadata:', response.metadata);
        
        // 🚨 Log si estamos en modo emergencia
        if (response.isEmergency) {
          console.warn('⚠️ Respuesta desde modo de emergencia');
        }

        // Si hay función del padre, llamarla
        if (onSendMessage) {
          onSendMessage(message.trim(), response);
        }

        // 🧹 Limpiar input
        setMessage('');
      } catch (error) {
        console.error('❌ Error:', error.message);
        // Solo mostrar alert para errores que no sean de conexión
        // (el modo emergencia ya maneja los errores de conexión)
        if (error.name !== 'AbortError') {
          console.warn('Error no manejado:', error.message);
        }
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="message-input-container">
      <form onSubmit={handleSubmit} className="message-form">
        <div className="input-wrapper">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={language === 'es' ? '💡 Ejemplos: "¿Qué stacks usas?", "¿Trabajas con startups?"':'💡 Examples: "Which stacks do you use?" "Do you work with startups?"'}
            className="message-input"
            disabled={isLoading}
          />

          <div className="action-buttons"> 
            <button 
              type="submit" 
              className="action-button send-button"
              disabled={!message.trim() || isLoading}
              title={language === 'es' ? 'Enviar mensaje' : 'Send message'}
            >
              {isLoading ? (
                <div className="loading-spinner">⏳</div>
              ) : (
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="20" 
                  height="20" 
                  viewBox="0 0 24 24" 
                  style={{ color: 'white' }}
                >
                  <path 
                    d="M2 21l21-9L2 3v7l15 2-15 2v7z"
                    fill="white"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Micro-animación "Heily está pensando..." */}
      {isLoading && (
        <div className="heily-typing-indicator">
          <span>{language === 'es' ? 'Heily está pensando' : 'Heily is thinking'}</span>
          <span className="typing-dots">
            <span>.</span><span>.</span><span>.</span>
          </span>
        </div>
      )}

      <div className="input-footer">
        <p className="disclaimer">
          {language === 'es' 
            ? 'Simulación con datos reales de mi portfolio'
            : 'Simulation with real data from my portfolio'
          }
        </p>
      </div>
    </div>
  );
};

export default MessageInput;
