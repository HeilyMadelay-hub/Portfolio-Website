import React, { useState } from 'react';
import './MessageInput.css';
import chatService from '../../../services/chat/chatServicio'; // Chat service

const MessageInput = ({ language, onSendMessage }) => {
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (message.trim() && !isLoading) {
            setIsLoading(true);
            try {
                // 📤 Call the service (now includes automatic emergency mode)
                const response = await chatService.sendMessage(
                    message.trim(),
                    'sobreheily' // Change according to the section you need
                );
                console.log('✅ Bot responded:', response.response);
                console.log('📊 Metadata:', response.metadata);

                // 🚨 Log if we're in emergency mode
                if (response.isEmergency) {
                    console.warn('⚠️ Response from emergency mode');
                }

                // If there's a parent function, call it
                if (onSendMessage) {
                    onSendMessage(message.trim(), response);
                }

                // 🧹 Clear input
                setMessage('');
            } catch (error) {
                console.error('❌ Error:', error.message);
                // Only show alert for errors that are not connection errors
                // (emergency mode already handles connection errors)
                if (error.name !== 'AbortError') {
                    console.warn('Unhandled error:', error.message);
                }
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div className="message-input-container">
            <form onSubmit={handleSubmit} className="message-form">
                <div className="input-wrapper">
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder={language === 'es' ? '💡 Examples: "What stacks do you use?", "Do you work with startups?"' : '💡 Examples: "Which stacks do you use?" "Do you work with startups?"'}
                        className="message-input"
                        disabled={isLoading}
                    />
                    <div className="action-buttons">
                        <button
                            type="submit"
                            className="action-button send-button"
                            disabled={!message.trim() || isLoading}
                            title={language === 'es' ? 'Send message' : 'Send message'}
                        >
                            {isLoading ? (
                                <div className="loading-spinner">⏳</div>
                            ) : (
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    style={{ color: 'white' }}
                                >
                                    <path
                                        d="M2 21l21-9L2 3v7l15 2-15 2v7z"
                                        fill="white"
                                    />
                                </svg>
                            )}
                        </button>
                    </div>
                </div>
            </form>

            {/* Micro-animation "Heily is thinking..." */}
            {isLoading && (
                <div className="heily-typing-indicator">
                    <span>{language === 'es' ? 'Heily is thinking' : 'Heily is thinking'}</span>
                    <span className="typing-dots">
                        <span>.</span><span>.</span><span>.</span>
                    </span>
                </div>
            )}

            <div className="input-footer">
                <p className="disclaimer">
                    {language === 'es'
                        ? 'Simulation with real data from my portfolio'
                        : 'Simulation with real data from my portfolio'
                    }
                </p>
            </div>
        </div>
    );
};

export default MessageInput;