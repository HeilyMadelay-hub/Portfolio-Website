import React, { useState } from 'react';
import './MessageInput.css';
import chatService from '../../services/chatServicio'; // Servicio de chat

const MessageInput = ({ language, onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      setIsLoading(true);

      try {
        // 📤 Llamar al servicio
        const response = await chatService.sendMessage(
          message.trim(),
          'sobreheily' // Cambia según la sección que necesites
        );

        console.log('✅ Bot respondió:', response.response);
        console.log('📊 Metadata:', response.metadata);

        // Si hay función del padre, llamarla
        if (onSendMessage) {
          onSendMessage(message.trim(), response);
        }

        // 🧹 Limpiar input
        setMessage('');
      } catch (error) {
        console.error('❌ Error:', error.message);
        alert(`Error: ${error.message}`);
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
            placeholder={language === 'es' ? 'Pregunta a MadGPT...' : 'Ask MadGPT...'}
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

      <div className="input-footer">
        <p className="disclaimer">
          {language === 'es' 
            ? 'Conóceme en solo 3 minutos'
            : 'Get to know me in just 3 minutes'
          }
        </p>
      </div>
    </div>
  );
};

export default MessageInput;
