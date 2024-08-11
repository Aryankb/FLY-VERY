import React, { useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Login from './components/Login';
import Signup from './components/Signup';

const App = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [activeCard, setActiveCard] = useState(null); // New state for active card

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  const openLoginCard = () => {
    setActiveCard('login');
  };

  const openSignupCard = () => {
    setActiveCard('signup');
  };

  const closeCard = () => {
    setActiveCard(null);
  };

  return (
    <div className="App">
      <img 
        src="/logo.png" 
        alt="Logo" 
        className="logo" 
        onClick={toggleSidebar} 
      />
      <Sidebar 
        isOpen={isSidebarOpen} 
        toggleSidebar={toggleSidebar}
        onAddCity={() => {/* handle add city */}} 
      />
      <div className="header">
        <h1>FLI - VERY</h1>
        <p>We deliver safe, secure and quick</p>
      </div>
      <div className="buttons">
        <button className="button" onClick={openLoginCard}>Login</button>
        <button className="button" onClick={openSignupCard}>Signup</button>
      </div>
      {activeCard === 'login' && <Login onClose={closeCard} />}
      {activeCard === 'signup' && <Signup onClose={closeCard} />}
      <div className="footer">
        © Fli-very, All rights reserved
      </div>
    </div>
  );
};

export default App;
