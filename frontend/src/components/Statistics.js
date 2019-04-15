import React from 'react';
import { FiCheckCircle, FiClock, FiTrendingUp, FiLayers, FiTag } from 'react-icons/fi';
import './Statistics.css';

function Statistics({ statistics }) {
  if (!statistics) {
    return (
      <div className="statistics-loading">
        <p>Loading statistics...</p>
      </div>
    );
  }

  const { total, pending, completed, completion_rate, by_priority, by_category } = statistics;

  return (
    <div className="statistics-container">
      <div className="stats-overview">
        <div className="stat-card">
          <div className="stat-icon">
            <FiLayers />
          </div>
          <div className="stat-content">
            <h3>Total Tasks</h3>
            <p className="stat-value">{total}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon pending">
            <FiClock />
          </div>
          <div className="stat-content">
            <h3>Pending</h3>
            <p className="stat-value">{pending}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon completed">
            <FiCheckCircle />
          </div>
          <div className="stat-content">
            <h3>Completed</h3>
            <p className="stat-value">{completed}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon rate">
            <FiTrendingUp />
          </div>
          <div className="stat-content">
            <h3>Completion Rate</h3>
            <p className="stat-value">{completion_rate}%</p>
          </div>
        </div>
      </div>

      <div className="stats-breakdown">
        <div className="breakdown-section">
          <h3><FiTag /> By Priority</h3>
          {Object.keys(by_priority).length > 0 ? (
            <div className="breakdown-list">
              {Object.entries(by_priority).map(([priority, count]) => (
                <div key={priority} className="breakdown-item">
                  <span className={`priority-label priority-${priority}`}>
                    {priority.charAt(0).toUpperCase() + priority.slice(1)}
                  </span>
                  <span className="breakdown-count">{count}</span>
                  <div className="breakdown-bar">
                    <div 
                      className={`bar-fill priority-${priority}`}
                      style={{ width: `${(count / total) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data">No tasks with priority</p>
          )}
        </div>

        <div className="breakdown-section">
          <h3><FiLayers /> By Category</h3>
          {Object.keys(by_category).length > 0 ? (
            <div className="breakdown-list">
              {Object.entries(by_category)
                .sort((a, b) => b[1] - a[1])
                .map(([category, count]) => (
                <div key={category} className="breakdown-item">
                  <span className="category-label">{category}</span>
                  <span className="breakdown-count">{count}</span>
                  <div className="breakdown-bar">
                    <div 
                      className="bar-fill"
                      style={{ width: `${(count / total) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data">No categorized tasks</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Statistics;