import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar = () => {
  const [activeSection, setActiveSection] = useState('nueva');
  
  const secciones = [
    { id: 'sobreheily', nombre: 'About Me', icono: '👩🏻‍💻' },
    { id: 'proyectos', nombre: 'Projects', icono: '⭐' },
    { id: 'articulo', nombre: 'Articles', icono: '📰' },
    { id: 'experiencia', nombre: 'Experience', icono: '⚒️' },
     { id: 'recomendaciones', nombre: 'Recommendations', icono: '📁' },
    { id: 'contacto', nombre: 'Contact', icono: '📞' }
  ];

  const conversacionesRecientes = [
    'Project discussion with Heily',
    'Articles of Heily'
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Sections</h2>
        <button className="menu-btn">☰</button>
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
        <h3>Recent conversations</h3>
        {conversacionesRecientes.map((conv, index) => (
          <div key={index} className="conversation-item">
            {conv}
          </div>
        ))}
      </div>

    </div>
  );
};

export default Sidebar;
