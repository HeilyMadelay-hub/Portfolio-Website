import React, { useState, useEffect } from 'react';
import './Sidebar.css';

const Sidebar = ({ language }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeSection, setActiveSection] = useState('nueva');

   const secciones = [
    { 
      id: 'sobreheily', 
      nombre: language === 'es' ? 'Sobre Mí' : 'About Me', 
      icono: '👩🏻‍💻' 
    },
    { 
      id: 'proyectos', 
      nombre: language === 'es' ? 'Proyectos' : 'Projects', 
      icono: '⭐' 
    },
    { 
      id: 'articulo', 
      nombre: language === 'es' ? 'Artículos' : 'Articles', 
      icono: '📰' 
    },
    { 
      id: 'experiencia', 
      nombre: language === 'es' ? 'Experiencia' : 'Experience', 
      icono: '⚒️' 
    },
    { 
      id: 'recomendaciones', 
      nombre: language === 'es' ? 'Recomendaciones' : 'Recommendations', 
      icono: '📁' 
    },
    { 
      id: 'contacto', 
      nombre: language === 'es' ? 'Contacto' : 'Contact', 
      icono: '📞' 
    }
  ];

  const conversacionesRecientes = language === 'es' 
    ? [
        'Discusión de proyecto con Heily',
        'Artículos de Heily'
      ]
    : [
        'Project discussion with Heily',
        'Articles of Heily'
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
          <h2>{language === 'es' ? 'Secciones' : 'Sections'}</h2>
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

        <div className="sidebar-sections">
          {secciones.map(seccion => (
            <div
              key={seccion.id}
              className={`sidebar-section ${activeSection === seccion.id ? 'active' : ''}`}
              onClick={() => setActiveSection(seccion.id)}
            >
              <span className="section-icon">{seccion.icono}</span>
              <span className="section-name">{seccion.nombre}</span>
            </div>
          ))}
        </div>

       
        <div className="recent-conversations">
          <h3>{language === 'es' ? 'Conversaciones recientes' : 'Recent conversations'}</h3>
          {conversacionesRecientes.map((conv, index) => (
            <div key={index} className="conversation-item">
              {conv}
            </div>
          ))}
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
