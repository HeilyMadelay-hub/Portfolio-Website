//Guardar el estado
//Organizar los componentes sidebar chat y input
//Pasa datos a hijos

//Usuario escribe la url
//- Por este archivo se carga el chat solo con / y con su sidebar,chatare y messageinput

import React, { useState, useEffect, useRef } from 'react';
import '../../App.css';
import Sidebar from '../../components/chat/Sidebar/Sidebar.jsx';
import ChatArea from '../../components/chat/ChatArea/ChatArea.jsx';
import MessageInput from '../../components/chat/MessageInput/MessageInput.jsx';
function App() {

    const [messages, setMessages] = useState([]);//useState hook de react que nos permite añadir estado local a un componente funcional tiene un array donde se guarda el mensaje y el estado
    const [activeSection, setActiveSection] = useState('nueva');// Estado para controlar la sección activa en la UI (por defecto 'nueva')
    const sidebarRef = useRef(null);// Referencia a la barra lateral, útil para manipularla directamente en el DOM

    //Agregar al estado un nuevo mensaje del usuario y la respuesta correspondiente del bot 
    const handleSendMessage = (message, response) => {
        //Se usa el estado previo de la conversacion y sobre el estado previo con el spreed operator añadimos al usuario y bot
        //para no perder mensajes agregados
        setMessages(prev => [...prev,
        { type: 'user', content: message },//El mensaje enviado por el usuario
        { type: 'bot', content: response.response, metadata: response.metadata }//La respuesta del bot con su info adicional,en este caso vector / ref al doc o tags
        ]);


    };

    const handleSectionClick = (sectionId) => {

        setActiveSection(sectionId);
        // Scroll suave al sidebar si está colapsado
        const sidebarElement = document.querySelector('.sidebar');
        if (sidebarElement?.classList.contains('collapsed')) {
            // Abrir sidebar
            sidebarElement.classList.remove('collapsed');
        }
        // Scroll suave a la sección en el sidebar
        setTimeout(() => {
            const sectionElement = document.querySelector(`[data-section-id="${sectionId}"]`);
            if (sectionElement) {
                sectionElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                sectionElement.classList.add('highlight');
                setTimeout(() => sectionElement.classList.remove('highlight'), 1500);
            }
        }, 100);

    };

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
            <Sidebar
                language={language}
                setLanguage={setLanguage}
                activeSection={activeSection}
                onSectionChange={setActiveSection}
            />
            <div className="main-container">
                <div className="chat-wrapper">
                    <ChatArea
                        language={language}
                        setLanguage={setLanguage}
                        messages={messages}
                        onSectionClick={handleSectionClick}
                    />
                    <MessageInput
                        language={language}
                        onSendMessage={handleSendMessage}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;
