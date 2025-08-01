import React from 'react';
import './App.css';
import Sidebar from './components/Sidebar/Sidebar.jsx';
import ChatArea from './components/ChatArea/ChatArea.jsx';
import MessageInput from './components/MessageInput/MessageInput.jsx';

function App() {
  return (
    <div className="app">
      <Sidebar />
      <div className="main-container">
        <ChatArea />
        <MessageInput />
      </div>
    </div>
  );
}

export default App;
