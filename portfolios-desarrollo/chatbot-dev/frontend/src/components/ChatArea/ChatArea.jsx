import React from 'react';
import './ChatArea.css';

const ChatArea = () => {
  return (
    <div className="chat-area">
      <div className="chat-header">
        <div className="chat-logo-container">

          <a 
            href="https://www.linkedin.com/in/heilymajtan/" 
            target="_blank" 
            rel="noopener noreferrer"
            style={{ display: 'inline-block' }}
          >
            <div className="chat-logo-circle">
              <img 
                src="/logo.png" 
                alt="MadGPT" 
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <span className="logo-placeholder" style={{display: 'none'}}>M</span>
            </div>
          </a>

          <h1 className="chat-title">Mad-GPT</h1>
          <p className="tagline">Backend Developer | AI Developer</p>
          <p className="tagline2"><em>Helping companies build scalable AI solutions</em></p>


        </div>
      </div>
    </div>
  );
};

export default ChatArea;






