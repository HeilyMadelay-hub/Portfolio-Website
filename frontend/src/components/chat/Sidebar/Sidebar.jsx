import React, { useState, useEffect } from 'react';
import './Sidebar.css';

const Sidebar = ({ language, setLanguage, activeSection: externalActiveSection, onSectionChange }) => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [internalActiveSection, setInternalActiveSection] = useState('nueva');

    // Use external section if exists, otherwise internal
    const activeSection = externalActiveSection || internalActiveSection;

    const handleSectionClick = (sectionId) => {
        if (onSectionChange) {
            onSectionChange(sectionId);
        } else {
            setInternalActiveSection(sectionId);
        }
    };

    const conversacionesRecientes = [
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

    const handleRename = (e, convId) => {
        e.stopPropagation();
        console.log('Rename conversation:', convId);
        // Add your rename logic here
        const newName = prompt('Enter new name for this conversation:');
        if (newName && newName.trim()) {
            console.log('New name:', newName);
            // Update conversation name logic here
        }
    };

    const handlePin = (e, convId) => {
        e.stopPropagation();
        console.log('Pin conversation:', convId);
        // Add your pin logic here
    };

    const handleDelete = (e, convId) => {
        e.stopPropagation();
        console.log('Delete conversation:', convId);
        // Add your delete logic here
        if (confirm('Are you sure you want to delete this conversation?')) {
            console.log('Conversation deleted:', convId);
        }
    };

    return (
        <>
            <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
                <div className="sidebar-header">
                    <h2>Recents</h2>
                    <button
                        className="menu-btn"
                        onClick={toggleSidebar}
                        title="Hide menu"
                        type="button"
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </button>
                </div>

                {/* New Conversation Button */}
                <div className="new-conversation-wrapper">
                    <button className="new-conversation-btn" onClick={() => handleSectionClick('nueva')}>
                        <span className="new-conv-icon">➕</span>
                        <span className="new-conv-text">New conversation</span>
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
                                <button
                                    className="action-btn rename-btn"
                                    onClick={(e) => handleRename(e, conv.id)}
                                    title="Rename conversation"
                                    aria-label="Rename conversation"
                                >
                                    <svg className="rename-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                                    </svg>
                                </button>
                                <button
                                    className="action-btn pin-btn"
                                    onClick={(e) => handlePin(e, conv.id)}
                                    title="Pin conversation"
                                    aria-label="Pin conversation"
                                >
                                    <svg className="pin-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M16 12V4h1c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1h1v8l-2 2v2h5.2v6h1.6v-6H18v-2l-2-2z" />
                                    </svg>
                                </button>
                                <button
                                    className="action-btn delete-btn"
                                    onClick={(e) => handleDelete(e, conv.id)}
                                    title="Delete conversation"
                                    aria-label="Delete conversation"
                                >
                                    <svg className="delete-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                                    </svg>
                                </button>
                            </span>
                        </div>
                    ))}
                </div>

               

            </div>

            {/* Floating button ALWAYS CLICKABLE */}
            {isCollapsed && (
                <div
                    className="floating-menu-btn"
                    onClick={handleFloatingClick}
                    onMouseDown={(e) => e.preventDefault()}
                    role="button"
                    tabIndex={0}
                    aria-label="Open menu"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>
            )}
        </>
    );
};

export default Sidebar;