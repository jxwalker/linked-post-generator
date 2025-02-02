import React, { useState } from 'react';
import { generatePosts } from '../services/apiService';
import SearchBar from './SearchBar';
import SearchResults from './SearchResults';
import './PostBuilder.css';

const PostBuilder = () => {
  const [sources, setSources] = useState([]);
  const [platforms, setPlatforms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generatedPosts, setGeneratedPosts] = useState(null);
  const [error, setError] = useState(null);

  const handleSourceAdd = (source) => {
    setSources([...sources, source]);
  };

  const handlePlatformToggle = (platform) => {
    if (platforms.includes(platform)) {
      setPlatforms(platforms.filter(p => p !== platform));
    } else {
      setPlatforms([...platforms, platform]);
    }
  };

  const handleGenerate = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await generatePosts(sources, platforms);
      setGeneratedPosts(result.posts);
    } catch (err) {
      setError('Failed to generate posts. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="post-builder">
      <h2>Create New Posts</h2>
      
      <div className="source-section">
        <h3>Select Sources</h3>
        <SearchBar onSourceAdd={handleSourceAdd} />
        <SearchResults sources={sources} onRemove={(url) => 
          setSources(sources.filter(s => s !== url))
        } />
      </div>

      <div className="platform-section">
        <h3>Select Platforms</h3>
        <div className="platform-toggles">
          <button
            className={`platform-btn ${platforms.includes('linkedin') ? 'active' : ''}`}
            onClick={() => handlePlatformToggle('linkedin')}
          >
            LinkedIn
          </button>
          <button
            className={`platform-btn ${platforms.includes('twitter') ? 'active' : ''}`}
            onClick={() => handlePlatformToggle('twitter')}
          >
            Twitter
          </button>
        </div>
      </div>

      <button 
        className="generate-btn"
        onClick={handleGenerate}
        disabled={loading || sources.length === 0 || platforms.length === 0}
      >
        {loading ? 'Generating...' : 'Generate Posts'}
      </button>

      {error && <div className="error-message">{error}</div>}

      {generatedPosts && (
        <div className="generated-posts">
          <h3>Generated Posts</h3>
          {Object.entries(generatedPosts).map(([platform, content]) => (
            <div key={platform} className="post-preview">
              <h4>{platform}</h4>
              <pre>{content}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PostBuilder; 