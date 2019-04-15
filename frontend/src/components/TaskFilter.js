import React from 'react';
import { FiFilter, FiTrash } from 'react-icons/fi';
import './TaskFilter.css';

function TaskFilter({ filters, onChange, onClearCompleted }) {
  const handleFilterChange = (field, value) => {
    onChange({
      ...filters,
      [field]: value
    });
  };

  return (
    <div className="task-filter">
      <div className="filter-group">
        <FiFilter className="filter-icon" />
        
        <div className="filter-item">
          <label htmlFor="status-filter">Status:</label>
          <select
            id="status-filter"
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
          >
            <option value="all">All Tasks</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div className="filter-item">
          <label htmlFor="priority-filter">Priority:</label>
          <select
            id="priority-filter"
            value={filters.priority}
            onChange={(e) => handleFilterChange('priority', e.target.value)}
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="filter-item">
          <label htmlFor="category-filter">Category:</label>
          <input
            type="text"
            id="category-filter"
            value={filters.category}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            placeholder="Filter by category"
          />
        </div>
      </div>

      <button onClick={onClearCompleted} className="btn-clear-completed">
        <FiTrash /> Clear Completed
      </button>
    </div>
  );
}

export default TaskFilter;