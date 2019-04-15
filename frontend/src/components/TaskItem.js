import React, { useState } from 'react';
import { FiCheck, FiTrash2, FiEdit2, FiSave, FiX } from 'react-icons/fi';
import './TaskItem.css';

function TaskItem({ task, isEditing, onComplete, onDelete, onEdit, onSave, onCancel }) {
  const [editedTask, setEditedTask] = useState({
    description: task.description,
    priority: task.priority,
    category: task.category
  });

  const handleInputChange = (field, value) => {
    setEditedTask(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = () => {
    if (editedTask.description.trim()) {
      onSave(editedTask);
    }
  };

  const priorityClass = `priority-${task.priority}`;
  const statusClass = task.status === 'completed' ? 'completed' : '';

  if (isEditing) {
    return (
      <div className={`task-item editing ${statusClass} ${priorityClass}`}>
        <div className="task-edit-form">
          <input
            type="text"
            value={editedTask.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            className="edit-input"
            placeholder="Task description"
          />
          <select
            value={editedTask.priority}
            onChange={(e) => handleInputChange('priority', e.target.value)}
            className="edit-select"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <input
            type="text"
            value={editedTask.category}
            onChange={(e) => handleInputChange('category', e.target.value)}
            className="edit-input"
            placeholder="Category"
          />
          <div className="edit-actions">
            <button onClick={handleSave} className="btn-save" title="Save">
              <FiSave />
            </button>
            <button onClick={onCancel} className="btn-cancel" title="Cancel">
              <FiX />
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`task-item ${statusClass} ${priorityClass}`}>
      <div className="task-checkbox">
        <input
          type="checkbox"
          checked={task.status === 'completed'}
          onChange={onComplete}
          disabled={task.status === 'completed'}
        />
      </div>
      <div className="task-content">
        <p className="task-description">{task.description}</p>
        <div className="task-meta">
          <span className="task-category">{task.category}</span>
          <span className={`task-priority ${priorityClass}`}>{task.priority}</span>
          <span className="task-id">#{task.id}</span>
        </div>
      </div>
      <div className="task-actions">
        {task.status !== 'completed' && (
          <>
            <button onClick={onComplete} className="btn-complete" title="Complete">
              <FiCheck />
            </button>
            <button onClick={onEdit} className="btn-edit" title="Edit">
              <FiEdit2 />
            </button>
          </>
        )}
        <button onClick={onDelete} className="btn-delete" title="Delete">
          <FiTrash2 />
        </button>
      </div>
    </div>
  );
}

export default TaskItem;