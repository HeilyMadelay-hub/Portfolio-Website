import React, { useEffect, useRef } from 'react';
import './MessageList.css';

const MessageList = ({ messages = [], language }) => {
  // Ref para scroll automático
  const messagesEndRef = useRef(null);

  // Scroll automático cuando cambian los mensajes
  useEffect(() => {
    const timer = setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ 
        behavior: "smooth",
        block: "end"
      });
    }, 100);
    
    return () => clearTimeout(timer);
  }, [messages]);

  return (
    <div className="messages-container">
      {/* Mensaje de bienvenida contextual */}
      {messages.length === 0 && (
        <div className="welcome-chat-message">
          <div className="message-avatar bot-avatar">
            <img 
              src="/logo.png" 
              alt="Heily" 
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
            <span className="avatar-fallback" style={{display: 'none'}}>H</span>
          </div>
          <div className="welcome-bubble">
            <p>{language === 'es' ? 'Hola 👋 Soy Heily.' : 'Hi 👋 I am Heily.'}</p>
            <p>
              {language === 'es'
                ? 'Soy desarrolladora Full Stack & MultiCloud. Puedes preguntarme sobre mi trabajo, proyectos o experiencia.'
                : 'I am a Full Stack & MultiCloud developer. Feel free to ask me anything about my work, projects or experience'}
            </p>
            <p className="welcome-cta">
              {language === 'es' ? '¿Qué te gustaría saber?' : 'What would you like to know?'}
            </p>
          </div>
        </div>
      )}

      {/* Renderizado de mensajes con animaciones */}
      {messages.map((msg, index) => (
        <div key={index} className={`message-wrapper ${msg.type}`}>
          {msg.type === 'bot' && (
            <div className="message-avatar bot-avatar">
              <img 
                src="/logo.png" 
                alt="Heily" 
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }}
              />
              <span className="avatar-fallback" style={{display: 'none'}}>H</span>
            </div>
          )}
          
          <div className={`message ${msg.type}`}>
            <div className="message-content">
              {msg.content}
            </div>
            {msg.metadata && (
              <div className="message-metadata">
                <small>{msg.metadata.source || ''}</small>
              </div>
            )}
          </div>
          
          {msg.type === 'user' && (
            <div className="message-avatar user-avatar">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="8" r="4" fill="currentColor"/>
                <path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
          )}
        </div>
      ))}

      {/* Elemento invisible para scroll automático */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;