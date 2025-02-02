import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <NavLink 
          to="/" 
          className={({ isActive }) => 
            `sidebar-link ${isActive ? 'active' : ''}`
          }
          end
        >
          <div className="sidebar-link-content">
            <i className="fas fa-home"></i>
            <span>Dashboard</span>
          </div>
        </NavLink>
        
        <NavLink 
          to="/post-builder" 
          className={({ isActive }) => 
            `sidebar-link ${isActive ? 'active' : ''}`
          }
        >
          <div className="sidebar-link-content">
            <i className="fas fa-pen"></i>
            <span>Create Post</span>
          </div>
        </NavLink>
        
        <NavLink 
          to="/scheduler" 
          className={({ isActive }) => 
            `sidebar-link ${isActive ? 'active' : ''}`
          }
        >
          <div className="sidebar-link-content">
            <i className="fas fa-clock"></i>
            <span>Schedule Posts</span>
          </div>
        </NavLink>
        
        <NavLink 
          to="/history" 
          className={({ isActive }) => 
            `sidebar-link ${isActive ? 'active' : ''}`
          }
        >
          <div className="sidebar-link-content">
            <i className="fas fa-history"></i>
            <span>Post History</span>
          </div>
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar; 