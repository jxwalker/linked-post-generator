import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getPostHistory } from '../services/apiService';
import PostBuilder from '../components/PostBuilder';
import './Dashboard.css';

const Dashboard = () => {
  const [recentPosts, setRecentPosts] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    published: 0,
    failed: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getPostHistory(1, 5); // Get 5 most recent posts
        setRecentPosts(response.data);
        
        // Calculate stats
        const total = response.data.length;
        const published = response.data.filter(post => post.status === 'published').length;
        const failed = response.data.filter(post => post.status === 'failed').length;
        
        setStats({ total, published, failed });
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome to Linked Post Generator</h1>
        <p>Generate and schedule social media posts from your favorite news sources</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <i className="fas fa-file-alt"></i>
          <div className="stat-content">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total Posts</span>
          </div>
        </div>
        
        <div className="stat-card">
          <i className="fas fa-check-circle"></i>
          <div className="stat-content">
            <span className="stat-value">{stats.published}</span>
            <span className="stat-label">Published</span>
          </div>
        </div>
        
        <div className="stat-card">
          <i className="fas fa-exclamation-circle"></i>
          <div className="stat-content">
            <span className="stat-value">{stats.failed}</span>
            <span className="stat-label">Failed</span>
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Quick Post</h2>
          </div>
          <PostBuilder />
        </div>
        
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Recent Posts</h2>
            <Link to="/history" className="view-all-link">
              View All <i className="fas fa-arrow-right"></i>
            </Link>
          </div>
          
          {loading ? (
            <div className="loading">Loading recent posts...</div>
          ) : (
            <div className="recent-posts">
              {recentPosts.map(post => (
                <div key={post.id} className="recent-post-item">
                  <div className="post-meta">
                    <span className={`status status-${post.status}`}>
                      {post.status}
                    </span>
                    <span className="platform">{post.platform}</span>
                    <span className="date">
                      {new Date(post.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="post-preview">
                    {post.content.substring(0, 100)}...
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 