import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          Linked Post Generator
        </Link>
        
        <nav className="nav-links">
          <Link to="/" className="nav-link">Dashboard</Link>
          <a 
            href="https://github.com/yourusername/linked-post-generator" 
            target="_blank" 
            rel="noopener noreferrer"
            className="nav-link"
          >
            GitHub
          </a>
        </nav>
      </div>
    </header>
  );
};

export default Header; 