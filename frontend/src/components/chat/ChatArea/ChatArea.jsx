import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChatArea.css';
import MessageList from './MessageList/MessageList';

const ChatArea = ({ language, setLanguage, messages = [], onSendMessage, onSectionClick }) => {

    const navigate = useNavigate();
    const [displayedText, setDisplayedText] = useState('');
    const [showCursor, setShowCursor] = useState(true);

    const tagline = 'Helping companies build scalable AI solutions';

    // Typewriter effect
    useEffect(() => {
        setDisplayedText('');
        let currentIndex = 0;

        const typeInterval = setInterval(() => {
            if (currentIndex <= tagline.length) {
                setDisplayedText(tagline.slice(0, currentIndex));
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
    }, [tagline]);

    const handleViewProjects = () => {
        navigate('/portfolio');
    };

    const handleContact = () => {
        window.location.href = 'mailto:heilymadelayajtan@icloud.com?subject=Hello Heily - New Project';
    };

    return (
        <div className="chat-area">
            {/* Header only shows when there are no messages */}
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
                                    <span className="logo-placeholder" style={{ display: 'none' }}>H</span>
                                </div>
                            </a>
                        </div>

                        <div className="hero-info-section">
                            <h1 className="chat-title-gradient">Heily Madelay Tandazo</h1>
                            <p className="hero-subtitle">Full Stack & MultiCloud Developer</p>

                            <div className="hero-availability">
                                <span className="availability-dot"></span>
                                <span>Available</span>
                            </div>

                            <div className="hero-buttons">
                                <button className="hero-btn hero-btn-primary" onClick={handleViewProjects}>
                                    View Professional Portfolio
                                </button>
                                <button className="hero-btn hero-btn-secondary" onClick={handleContact}>
                                    Let's Talk
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

            {/* MessageList handles all message rendering */}
            <MessageList messages={messages} language={language} />
        </div>
    );
};

export default ChatArea;