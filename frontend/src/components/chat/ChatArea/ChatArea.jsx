import React, { useState, useEffect } from 'react';
import './ChatArea.css';
import MessageList from './MessageList/MessageList'; // Import del componente

const ChatArea = ({ language, setLanguage, messages = [], onSendMessage, onSectionClick }) => {
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
    }, 50);
    
    const cursorInterval = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 500);
    
    return () => {
      clearInterval(typeInterval);
      clearInterval(cursorInterval);
    };
  }, [currentTagline, language]);

  const handleViewProjects = () => {
    window.location.href = '/portfolio';
  };

  const handleContact = () => {
    window.location.href = 'mailto:heilymadelayajtan@icloud.com?subject=Hola Heily - Nuevo Proyecto';
  };

  return (
    <div className="chat-area">
      {/* Header solo se muestra si no hay mensajes */}
      {messages.length === 0 && (
        <div className="chat-header">
          <div className="gradient-bg"></div>
          <div className="hero-container">
            <div className="hero-photo-section">
              <a 
                href="https://www.linkedin.com/in/heilymajtan/" 
                target="_blank" 
                rel="noopener noreferrer"
              >
                <div className="chat-logo-circle">
                  <img 
                    src="/logo.png" 
                    alt="Heily Madelay Tandazo" 
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  <span className="logo-placeholder" style={{display: 'none'}}>H</span>
                </div>
              </a>
            </div>

            <div className="hero-info-section">
              <h1 className="chat-title-gradient">Heily Madelay Tandazo</h1>
              <p className="hero-subtitle">{language === 'es' ? 'Desarrolladora Full Stack & MultiCloud' : 'Full Stack & MultiCloud Developer'}</p>
              
              <div className="hero-availability">
                <span className="availability-dot"></span>
                <span>{language === 'es' ? 'Disponible' : 'Available'}</span>
              </div>
              
              <div className="hero-buttons">
                <button className="hero-btn hero-btn-primary" onClick={handleViewProjects}>
                  {language === 'es' ? 'Ver Portfolio Profesional' : 'View Professional Portfolio'}
                </button>
                <button className="hero-btn hero-btn-secondary" onClick={handleContact}>
                  {language === 'es' ? 'Hablemos' : "Let's Talk"}
                </button>
              </div>

              <div className="hero-social-links">
                <a href="https://github.com/HeilyMadelay-hub" target="_blank" rel="noopener noreferrer">GitHub</a>
                <a href="https://www.linkedin.com/in/heilymajtan/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                <a href="mailto:heilymadelayajtan@icloud.com">heilymadelayajtan@icloud.com</a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MessageList maneja todo el renderizado de mensajes */}
      <MessageList messages={messages} language={language} />
    </div>
  );
};

export default ChatArea;