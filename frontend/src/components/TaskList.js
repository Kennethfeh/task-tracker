import React, { useState } from 'react';
import TaskItem from './TaskItem';
import './TaskList.css';

function TaskList({ tasks, onComplete, onDelete, onUpdate }) {
  const [editingId, setEditingId] = useState(null);

  const handleEdit = (taskId) => {
    setEditingId(taskId);
  };

  const handleSave = (taskId, updates) => {
    onUpdate(taskId, updates);
    setEditingId(null);
  };

  const handleCancel = () => {
    setEditingId(null);
  };

  if (tasks.length === 0) {
    return (
      <div className="task-list-empty">
        <p>No tasks found. Create your first task above!</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map(task => (
        <TaskItem
          key={task.id}
          task={task}
          isEditing={editingId === task.id}
          onComplete={() => onComplete(task.id)}
          onDelete={() => onDelete(task.id)}
          onEdit={() => handleEdit(task.id)}
          onSave={(updates) => handleSave(task.id, updates)}
          onCancel={handleCancel}
        />
      ))}
    </div>
  );
}

export default TaskList;