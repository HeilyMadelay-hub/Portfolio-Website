import React, { useState, useEffect } from 'react';
import './Sidebar.css';

const Sidebar = ({ language, setLanguage, activeSection: externalActiveSection, onSectionChange }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [internalActiveSection, setInternalActiveSection] = useState('nueva');
  
  // Usar sección externa si existe, sino la interna
  const activeSection = externalActiveSection || internalActiveSection;
  
  const handleSectionClick = (sectionId) => {
    if (onSectionChange) {
      onSectionChange(sectionId);
    } else {
      setInternalActiveSection(sectionId);
    }
  };

 const conversacionesRecientes = language === 'es' 
    ? [
        { 
          id: 'proyecto', 
          nombre: 'Conversación sobre proyecto', // Más claro
          nombreCompleto: 'Conversación sobre proyecto con startup fintech', // Para tooltip
          icono: '💬' 
        },
        { 
          id: 'articulos', 
          nombre: 'Artículos técnicos', // Más específico
          nombreCompleto: 'Artículos técnicos que escribo',
          icono: '📝' 
        }
      ]
    : [
        { 
          id: 'proyecto', 
          nombre: 'Project conversation',
          nombreCompleto: 'Project conversation with fintech startup',
          icono: '💬' 
        },
        { 
          id: 'articulos', 
          nombre: 'Technical articles',
          nombreCompleto: 'Technical articles I write',
          icono: '📝' 
        }
      ];

  const toggleSidebar = () => {
    console.log('Toggle sidebar clicked!', !isCollapsed);
    setIsCollapsed(!isCollapsed);
  };

  const handleFloatingClick = (e) => {
    console.log('Floating button clicked!');
    e.preventDefault();
    e.stopPropagation();
    setIsCollapsed(false);
  };

  return (
    <>
      <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <h2>{language === 'es' ? 'Recientes' : 'Recents'}</h2>
          <button 
            className="menu-btn" 
            onClick={toggleSidebar} 
            title={language === 'es' ? 'Ocultar menú' : 'Hide menu'}
            type="button"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>

        {/* Botón Nueva Conversación */}
        <div className="new-conversation-wrapper">
          <button className="new-conversation-btn" onClick={() => handleSectionClick('nueva')}>
            <span className="new-conv-icon">➕</span>
            <span className="new-conv-text">{language === 'es' ? 'Nueva conversación' : 'New conversation'}</span>
          </button>
        </div>

        <div className="sidebar-sections">
          {conversacionesRecientes.map(conv => (
            <div
              key={conv.id}
              data-section-id={conv.id}
              className={`sidebar-section ${activeSection === conv.id ? 'active' : ''}`}
              onClick={() => handleSectionClick(conv.id)}
              onMouseEnter={e => e.currentTarget.classList.add('hovered')}
              onMouseLeave={e => e.currentTarget.classList.remove('hovered')}
              title={conv.nombreCompleto}
            >
              <span className="section-icon">{conv.icono}</span>
              <span className="section-name">{conv.nombre}</span>
              <span className="conversation-actions">
                <svg className="pin-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M16 12V4h1c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1h1v8l-2 2v2h5.2v6h1.6v-6H18v-2l-2-2z"/>
                </svg>
                <svg className="delete-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                </svg>
              </span>
            </div>
          ))}
        </div>

        {/* Selector de idioma */}
        <div className="sidebar-language-selector">
          <button 
            className={`language-option ${language === 'es' ? 'active' : ''}`}
            onClick={() => setLanguage && setLanguage('es')}
          >
            🇪🇸 Español
          </button>
          <button 
            className={`language-option ${language === 'en' ? 'active' : ''}`}
            onClick={() => setLanguage && setLanguage('en')}
          >
            🇬🇧 English
          </button>
        </div>

      </div>

      {/* Botón flotante SIEMPRE CLICKEABLE */}
      {isCollapsed && (
        <div 
          className="floating-menu-btn"
          onClick={handleFloatingClick}
          onMouseDown={(e) => e.preventDefault()}
          role="button"
          tabIndex={0}
          aria-label={language === 'es' ? 'Abrir menú' : 'Open menu'}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      )}
    </>
  );
};

export default Sidebar;