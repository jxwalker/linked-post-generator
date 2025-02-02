import React, { useState, useEffect } from 'react';
import { getPostHistory, deletePost } from '../services/apiService';
import './PostHistory.css';

const PostHistory = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await getPostHistory(page);
      const newPosts = response.data;
      
      setPosts(prev => [...prev, ...newPosts]);
      setHasMore(newPosts.length === 10); // Assuming page size is 10
    } catch (err) {
      setError('Failed to load post history');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [page]);

  const handleLoadMore = () => {
    setPage(prev => prev + 1);
  };

  const handleDelete = async (postId) => {
    try {
      await deletePost(postId);
      setPosts(posts.filter(post => post.id !== postId));
    } catch (err) {
      setError('Failed to delete post');
      console.error(err);
    }
  };

  return (
    <div className="post-history">
      <h2>Post History</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="posts-list">
        {posts.map(post => (
          <div key={post.id} className="post-item">
            <div className="post-header">
              <span className="platform">{post.platform}</span>
              <span className="date">
                {new Date(post.created_at).toLocaleDateString()}
              </span>
            </div>
            <pre className="content">{post.content}</pre>
            <div className="post-footer">
              <span className={`status status-${post.status}`}>
                {post.status}
              </span>
              <button
                className="delete-btn"
                onClick={() => handleDelete(post.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
      
      {loading && <div className="loading">Loading...</div>}
      
      {hasMore && !loading && (
        <button
          className="load-more-btn"
          onClick={handleLoadMore}
        >
          Load More
        </button>
      )}
    </div>
  );
};

export default PostHistory; 