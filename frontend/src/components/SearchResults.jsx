import React from 'react';
import './SearchResults.css';

const SearchResults = ({ sources, onRemove }) => {
  if (sources.length === 0) {
    return <div className="no-sources">No sources added yet</div>;
  }

  return (
    <div className="search-results">
      {sources.map((source, index) => (
        <div key={index} className="source-item">
          <span className="source-url">{source}</span>
          <button 
            className="remove-btn"
            onClick={() => onRemove(source)}
            aria-label="Remove source"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
};

export default SearchResults; 