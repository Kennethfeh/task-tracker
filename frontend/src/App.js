import React, { useState, useEffect } from 'react';
import './App.css';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import TaskFilter from './components/TaskFilter';
import Statistics from './components/Statistics';
import { apiClient } from './services/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [filters, setFilters] = useState({
    status: 'all',
    category: '',
    priority: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeView, setActiveView] = useState('tasks');

  // Load tasks on component mount and when filters change
  useEffect(() => {
    loadTasks();
    loadStatistics();
  }, [filters]);

  const loadTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getTasks(filters);
      setTasks(data.tasks);
    } catch (err) {
      setError('Failed to load tasks: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const data = await apiClient.getStatistics();
      setStatistics(data.statistics);
    } catch (err) {
      console.error('Failed to load statistics:', err);
    }
  };

  const handleAddTask = async (taskData) => {
    try {
      await apiClient.createTask(taskData);
      await loadTasks();
      await loadStatistics();
    } catch (err) {
      setError('Failed to add task: ' + err.message);
    }
  };

  const handleCompleteTask = async (taskId) => {
    try {
      await apiClient.completeTask(taskId);
      await loadTasks();
      await loadStatistics();
    } catch (err) {
      setError('Failed to complete task: ' + err.message);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await apiClient.deleteTask(taskId);
      await loadTasks();
      await loadStatistics();
    } catch (err) {
      setError('Failed to delete task: ' + err.message);
    }
  };

  const handleUpdateTask = async (taskId, updates) => {
    try {
      await apiClient.updateTask(taskId, updates);
      await loadTasks();
      await loadStatistics();
    } catch (err) {
      setError('Failed to update task: ' + err.message);
    }
  };

  const handleClearCompleted = async () => {
    if (window.confirm('Are you sure you want to clear all completed tasks?')) {
      try {
        await apiClient.clearCompleted();
        await loadTasks();
        await loadStatistics();
      } catch (err) {
        setError('Failed to clear completed tasks: ' + err.message);
      }
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Task Tracker</h1>
        <nav className="navigation">
          <button 
            className={activeView === 'tasks' ? 'active' : ''}
            onClick={() => setActiveView('tasks')}
          >
            Tasks
          </button>
          <button 
            className={activeView === 'statistics' ? 'active' : ''}
            onClick={() => setActiveView('statistics')}
          >
            Statistics
          </button>
        </nav>
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            {error}
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {activeView === 'tasks' ? (
          <>
            <TaskForm onSubmit={handleAddTask} />
            <TaskFilter 
              filters={filters} 
              onChange={handleFilterChange}
              onClearCompleted={handleClearCompleted}
            />
            {loading ? (
              <div className="loading">Loading tasks...</div>
            ) : (
              <TaskList 
                tasks={tasks}
                onComplete={handleCompleteTask}
                onDelete={handleDeleteTask}
                onUpdate={handleUpdateTask}
              />
            )}
          </>
        ) : (
          <Statistics statistics={statistics} />
        )}
      </main>
    </div>
  );
}

export default App;
