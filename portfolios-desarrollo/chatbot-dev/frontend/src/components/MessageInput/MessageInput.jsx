import React, { useState } from 'react';
import './MessageInput.css';

const MessageInput = ({ language }) => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      // Aquí enviarías el mensaje
      console.log('Enviando mensaje:', message);
      setMessage('');
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
          />

          <div className="action-buttons"> 
            <button 
              type="submit" 
              className="action-button send-button"
              disabled={!message.trim()}
              title={language === 'es' ? 'Enviar mensaje' : 'Send message'}
            >
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
