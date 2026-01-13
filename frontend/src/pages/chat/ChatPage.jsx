// Save state
// Organize sidebar, chat, and input components
// Pass data to children

// User writes the URL
// - This file loads the chat only with / and with its sidebar, chatarea and messageinput

import React, { useState, useEffect, useRef } from 'react';
import '../../App.css';
import Sidebar from '../../components/chat/Sidebar/Sidebar.jsx';
import ChatArea from '../../components/chat/ChatArea/ChatArea.jsx';
import MessageInput from '../../components/chat/MessageInput/MessageInput.jsx';

function App() {

    const [messages, setMessages] = useState([]); // useState hook from React that allows us to add local state to a functional component, has an array where the message and state are saved
    const [activeSection, setActiveSection] = useState('nueva'); // State to control the active section in the UI (default 'nueva')
    const sidebarRef = useRef(null); // Reference to the sidebar, useful for manipulating it directly in the DOM

    // Add to state a new user message and the corresponding bot response 
    const handleSendMessage = (message, response) => {
        // We use the previous conversation state and over the previous state with the spread operator we add the user and bot
        // to not lose added messages
        setMessages(prev => [...prev,
        { type: 'user', content: message }, // The message sent by the user
        { type: 'bot', content: response.response, metadata: response.metadata } // The bot's response with its additional info, in this case vector / ref to doc or tags
        ]);
    };

    const handleSectionClick = (sectionId) => {
        setActiveSection(sectionId);
        // Smooth scroll to sidebar if it's collapsed
        const sidebarElement = document.querySelector('.sidebar');
        if (sidebarElement?.classList.contains('collapsed')) {
            // Open sidebar
            sidebarElement.classList.remove('collapsed');
        }
        // Smooth scroll to section in sidebar
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

    // Listen to sidebar changes for browsers that don't support :has
    useEffect(() => {
        const checkSidebarState = () => {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                setSidebarCollapsed(sidebar.classList.contains('collapsed'));
            }
        };

        // Observe DOM changes
        const observer = new MutationObserver(checkSidebarState);
        const sidebar = document.querySelector('.sidebar');

        if (sidebar) {
            observer.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
        }

        // Initial check
        checkSidebarState();

        return () => observer.disconnect();
    }, []);

    return (
        <div className={`app ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
            <Sidebar
                activeSection={activeSection}
                onSectionChange={setActiveSection}
            />
            <div className="main-container">
                <div className="chat-wrapper">
                    <ChatArea
                        messages={messages}
                        onSectionClick={handleSectionClick}
                    />
                    <MessageInput
                        onSendMessage={handleSendMessage}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;