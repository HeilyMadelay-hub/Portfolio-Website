import React, { useState, useEffect } from 'react';
import './ChatArea.css';

const ChatArea = ({ language, setLanguage, messages = [] }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  
  const taglineES = 'Ayudando a empresas a construir soluciones IA escalables';
  const taglineEN = 'Helping companies build scalable AI solutions';
  const currentTagline = language === 'es' ? taglineES : taglineEN;
  
  // Efecto typewriter
  useEffect(() => {
    setDisplayedText('');
    let currentIndex = 0;
    
    const typeInterval = setInterval(() => {
      if (currentIndex <= currentTagline.length) {
        setDisplayedText(currentTagline.slice(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(typeInterval);
      }
    }, 50); // Velocidad de escritura
    
    // Cursor parpadeante
    const cursorInterval = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 500);
    
    return () => {
      clearInterval(typeInterval);
      clearInterval(cursorInterval);
    };
  }, [currentTagline, language]);
  return (
    <div className="chat-area">
      {/* Botón de traducción */}
      <button 
        className={`translate-button ${messages.length > 0 ? 'minimal' : ''}`}
        onClick={() => setLanguage(language === 'es' ? 'en' : 'es')}
        title={language === 'es' ? 'Switch to English' : 'Cambiar a Español'}
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12.87 15.07l-2.54-2.51.03-.03c1.74-1.94 2.98-4.17 3.71-6.53H17V4h-7V2H8v2H1v1.99h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z" fill="currentColor"/>
        </svg>
        <span className="translate-text">{language === 'es' ? 'EN' : 'ES'}</span>
      </button>
      
      {messages.length === 0 && (
        <div className="chat-header">
          <div className="gradient-bg"></div>
          <div className="chat-logo-container">

            <a 
              href="https://www.linkedin.com/in/heilymajtan/" 
              target="_blank" 
              rel="noopener noreferrer"
              style={{ display: 'inline-block' }}
            >
              <div className="chat-logo-circle">
                <img 
                  src="/logo.png" 
                  alt="MadGPT" 
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'block';
                  }}
                />
                <span className="logo-placeholder" style={{display: 'none'}}>M</span>
              </div>
            </a>

            <h1 className="chat-title">Mad-GPT</h1>
            <p className="tagline">{language === 'es' ? 'Desarrolladora Full Stack & MultiCloud ' : 'Full Stack & MultiCloud Developer'}</p>
            <p className="tagline2">
              <em>{displayedText}</em>
              <span className={`cursor ${showCursor ? 'visible' : ''}`}>|</span>
            </p>
          </div>
        </div>
      )}

      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-content">
              {msg.content}
            </div>
            {msg.metadata && (
              <div className="message-metadata">
                <small>{msg.metadata.source || ''}</small>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatArea;






