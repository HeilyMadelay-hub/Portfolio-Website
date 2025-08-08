import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar/Sidebar.jsx';
import ChatArea from './components/ChatArea/ChatArea.jsx';
import MessageInput from './components/MessageInput/MessageInput.jsx';

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [language, setLanguage] = useState('es'); // Estado global para el idioma

  // Escuchar cambios en el sidebar para browsers que no soportan :has
  useEffect(() => {
    const checkSidebarState = () => {
      const sidebar = document.querySelector('.sidebar');
      if (sidebar) {
        setSidebarCollapsed(sidebar.classList.contains('collapsed'));
      }
    };

    // Observar cambios en el DOM
    const observer = new MutationObserver(checkSidebarState);
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebar) {
      observer.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
    }

    // Check inicial
    checkSidebarState();

    return () => observer.disconnect();
  }, []);

  return (
    <div className={`app ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      <Sidebar language={language} />
      <div className="main-container">
        <ChatArea language={language} setLanguage={setLanguage} />
        <MessageInput language={language} />
      </div>
    </div>
  );
}

export default App;
