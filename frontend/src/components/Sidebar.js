import React from 'react';
import './Sidebar.css';

const Sidebar = ({ isOpen, toggleSidebar, onAddCity }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <button className="button" onClick={toggleSidebar}>Close</button>
      <button className="button" onClick={onAddCity}>Add City</button>
      <button className="button">Configure City</button>
      <button className="button">Show All Cities</button>
      <button className="button">Manage Orders</button>
    </div>
  );
};

export default Sidebar;
