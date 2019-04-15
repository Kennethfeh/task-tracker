import React, { useState } from 'react';
import { FiPlus } from 'react-icons/fi';
import './TaskForm.css';

function TaskForm({ onSubmit }) {
  const [task, setTask] = useState({
    description: '',
    priority: 'medium',
    category: 'general'
  });
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (task.description.trim()) {
      onSubmit(task);
      setTask({
        description: '',
        priority: 'medium',
        category: 'general'
      });
      setIsExpanded(false);
    }
  };

  const handleInputChange = (field, value) => {
    setTask(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="task-form-container">
      <form onSubmit={handleSubmit} className="task-form">
        <div className="form-main">
          <input
            type="text"
            value={task.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            placeholder="Add a new task..."
            className="task-input"
            onFocus={() => setIsExpanded(true)}
          />
          <button type="submit" className="btn-add" disabled={!task.description.trim()}>
            <FiPlus /> Add Task
          </button>
        </div>
        
        {isExpanded && (
          <div className="form-options">
            <div className="form-group">
              <label htmlFor="priority">Priority:</label>
              <select
                id="priority"
                value={task.priority}
                onChange={(e) => handleInputChange('priority', e.target.value)}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="category">Category:</label>
              <input
                type="text"
                id="category"
                value={task.category}
                onChange={(e) => handleInputChange('category', e.target.value)}
                placeholder="e.g., Work, Personal"
              />
            </div>
          </div>
        )}
      </form>
    </div>
  );
}

export default TaskForm;