import React, { useState } from 'react';
import { generatePosts } from '../services/apiService';
import SearchBar from './SearchBar';
import SearchResults from './SearchResults';
import './Scheduler.css';

const Scheduler = () => {
  const [sources, setSources] = useState([]);
  const [platforms, setPlatforms] = useState([]);
  const [schedule, setSchedule] = useState('0 9 * * *'); // Default: 9 AM daily
  const [notifyEmail, setNotifyEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleSchedule = async () => {
    try {
      setLoading(true);
      setError(null);
      await generatePosts(sources, platforms, schedule, notifyEmail);
      setSuccess(true);
    } catch (err) {
      setError('Failed to schedule posts. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scheduler">
      <h2>Schedule Recurring Posts</h2>
      
      <div className="source-section">
        <h3>Select Sources</h3>
        <SearchBar onSourceAdd={(source) => setSources([...sources, source])} />
        <SearchResults sources={sources} onRemove={(url) => 
          setSources(sources.filter(s => s !== url))
        } />
      </div>

      <div className="platform-section">
        <h3>Select Platforms</h3>
        <div className="platform-toggles">
          {['linkedin', 'twitter'].map(platform => (
            <button
              key={platform}
              className={`platform-btn ${platforms.includes(platform) ? 'active' : ''}`}
              onClick={() => {
                if (platforms.includes(platform)) {
                  setPlatforms(platforms.filter(p => p !== platform));
                } else {
                  setPlatforms([...platforms, platform]);
                }
              }}
            >
              {platform.charAt(0).toUpperCase() + platform.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="schedule-section">
        <h3>Set Schedule</h3>
        <input
          type="text"
          value={schedule}
          onChange={(e) => setSchedule(e.target.value)}
          placeholder="Cron expression (e.g., 0 9 * * *)"
        />
        <p className="schedule-help">Format: minute hour day month weekday</p>
      </div>

      <div className="notification-section">
        <h3>Notification Email</h3>
        <input
          type="email"
          value={notifyEmail}
          onChange={(e) => setNotifyEmail(e.target.value)}
          placeholder="Enter email for notifications"
        />
      </div>

      <button
        className="schedule-btn"
        onClick={handleSchedule}
        disabled={loading || sources.length === 0 || platforms.length === 0}
      >
        {loading ? 'Scheduling...' : 'Schedule Posts'}
      </button>

      {error && <div className="error-message">{error}</div>}
      {success && (
        <div className="success-message">
          Posts scheduled successfully! You will receive notifications at {notifyEmail}
        </div>
      )}
    </div>
  );
};

export default Scheduler; 