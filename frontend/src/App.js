import React, { useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';

const App = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="App">
      <img 
        src="/logo.png" 
        alt="Logo" 
        className="logo" 
        onClick={toggleSidebar} 
      />
      <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
      <div className="header">
        <h1>FLI - VERY</h1>
        <p>We deliver safe, secure and quick</p>
      </div>
      <div className="buttons">
        <button className="button">Login</button>
        <button className="button">Signup</button>
      </div>
      <div className="footer">
        © Fli-very, All rights reserved
      </div>
    </div>
  );
};

export default App;
