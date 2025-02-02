import React, { useState } from 'react';
import './SearchBar.css';

const SearchBar = ({ onSourceAdd }) => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Basic URL validation
    try {
      new URL(url);
      onSourceAdd(url);
      setUrl('');
      setError('');
    } catch {
      setError('Please enter a valid URL');
    }
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter RSS feed or news source URL"
        className={error ? 'error' : ''}
      />
      <button type="submit">Add Source</button>
      {error && <div className="error-message">{error}</div>}
    </form>
  );
};

export default SearchBar; 