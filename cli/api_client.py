"""
API Client for Task Tracker CLI to communicate with backend
"""

import requests
import json
from typing import List, Dict, Optional, Any


class TaskAPIClient:
    """Client for interacting with Task Tracker API."""
    
    def __init__(self, base_url: str = 'http://localhost:5001'):
        """Initialize the API client."""
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
    
    def _handle_response(self, response):
        """Handle API response and raise exceptions if needed."""
        try:
            data = response.json()
            if response.status_code >= 400:
                raise Exception(data.get('error', 'Unknown API error'))
            return data
        except json.JSONDecodeError:
            raise Exception(f"Invalid response from server: {response.text}")
    
    def add_task(self, description: str, priority: str = 'medium', 
                 category: str = 'general') -> int:
        """Add a new task via API."""
        response = requests.post(
            f"{self.api_url}/tasks",
            json={
                'description': description,
                'priority': priority,
                'category': category
            }
        )
        data = self._handle_response(response)
        return data['task']['id']
    
    def list_tasks(self, status: str = 'all', category: Optional[str] = None,
                   priority: Optional[str] = None) -> List[Dict[str, Any]]:
        """List tasks via API."""
        params = {'status': status}
        if category:
            params['category'] = category
        if priority:
            params['priority'] = priority
        
        response = requests.get(f"{self.api_url}/tasks", params=params)
        data = self._handle_response(response)
        return data['tasks']
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed via API."""
        response = requests.post(f"{self.api_url}/tasks/{task_id}/complete")
        data = self._handle_response(response)
        return data['success']
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task via API."""
        response = requests.delete(f"{self.api_url}/tasks/{task_id}")
        data = self._handle_response(response)
        return data['success']
    
    def update_task(self, task_id: int, description: Optional[str] = None,
                    priority: Optional[str] = None, 
                    category: Optional[str] = None) -> bool:
        """Update task via API."""
        update_data = {}
        if description:
            update_data['description'] = description
        if priority:
            update_data['priority'] = priority
        if category:
            update_data['category'] = category
        
        response = requests.put(
            f"{self.api_url}/tasks/{task_id}",
            json=update_data
        )
        data = self._handle_response(response)
        return data['success']
    
    def clear_completed(self) -> int:
        """Clear all completed tasks via API."""
        response = requests.post(f"{self.api_url}/tasks/clear-completed")
        data = self._handle_response(response)
        return data['count']
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get task statistics via API."""
        response = requests.get(f"{self.api_url}/statistics")
        data = self._handle_response(response)
        return data['statistics']
    
    def check_connection(self) -> bool:
        """Check if API is available."""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False