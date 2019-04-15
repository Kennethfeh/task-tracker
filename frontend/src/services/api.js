import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

class ApiClient {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async getTasks(filters = {}) {
    const params = new URLSearchParams();
    if (filters.status) params.append('status', filters.status);
    if (filters.category) params.append('category', filters.category);
    if (filters.priority) params.append('priority', filters.priority);
    
    const response = await this.client.get(`/tasks?${params}`);
    return response.data;
  }

  async createTask(taskData) {
    const response = await this.client.post('/tasks', taskData);
    return response.data;
  }

  async updateTask(taskId, updates) {
    const response = await this.client.put(`/tasks/${taskId}`, updates);
    return response.data;
  }

  async completeTask(taskId) {
    const response = await this.client.post(`/tasks/${taskId}/complete`);
    return response.data;
  }

  async deleteTask(taskId) {
    const response = await this.client.delete(`/tasks/${taskId}`);
    return response.data;
  }

  async clearCompleted() {
    const response = await this.client.post('/tasks/clear-completed');
    return response.data;
  }

  async getStatistics() {
    const response = await this.client.get('/statistics');
    return response.data;
  }
}

export const apiClient = new ApiClient();