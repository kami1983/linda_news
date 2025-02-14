import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css'; // 导入样式文件

function Navigation() {
  return (
    <nav className="navigation">
      <ul className="nav-list">
        <li className="nav-item">
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li className="nav-item">
          <Link to="/ainews" className="nav-link">AI News</Link>
        </li>
        <li className="nav-item">
          <Link to="/upload" className="nav-link">Knowledge Base</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation; 