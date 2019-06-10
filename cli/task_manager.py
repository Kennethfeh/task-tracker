"""
Task Manager module for handling task operations and JSON storage.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any


class TaskManager:
    """Manages tasks with JSON file storage."""
    
    def __init__(self, data_file: str = 'tasks.json'):
        """Initialize the TaskManager with a data file."""
        self.data_file = data_file
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file."""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r') as f:
                content = f.read()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load tasks file: {e}")
            return []
    
    def _save_tasks(self) -> bool:
        """Save tasks to JSON file."""
        try:
            # Create backup of existing file
            if os.path.exists(self.data_file):
                backup_file = f"{self.data_file}.backup"
                with open(self.data_file, 'r') as src, open(backup_file, 'w') as dst:
                    dst.write(src.read())
            
            # Write new data
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2, default=str)
            return True
        except IOError as e:
            raise Exception(f"Failed to save tasks: {e}")
    
    def _get_next_id(self) -> int:
        """Get the next available task ID."""
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1
    
    def add_task(self, description: str, priority: str = 'medium', 
                 category: str = 'general') -> int:
        """Add a new task."""
        # Input validation
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        # Sanitize inputs
        description = description.strip()
        category = category.strip() if category else 'general'
        
        task = {
            'id': self._get_next_id(),
            'description': description,
            'priority': priority,
            'category': category,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        self.tasks.append(task)
        self._save_tasks()
        return task['id']
    
    def list_tasks(self, status: str = 'all', category: Optional[str] = None,
                   priority: Optional[str] = None) -> List[Dict[str, Any]]:
        """List tasks with optional filters."""
        filtered_tasks = self.tasks.copy()
        
        # Filter by status
        if status != 'all':
            filtered_tasks = [t for t in filtered_tasks if t['status'] == status]
        
        # Filter by category
        if category:
            filtered_tasks = [t for t in filtered_tasks 
                            if t['category'].lower() == category.lower()]
        
        # Filter by priority
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t['priority'] == priority]
        
        # Sort by status (pending first) then by created date
        filtered_tasks.sort(key=lambda x: (x['status'] == 'completed', x['created_at']))
        
        return filtered_tasks
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                self._save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                self._save_tasks()
                return True
        return False
    
    def update_task(self, task_id: int, description: Optional[str] = None,
                    priority: Optional[str] = None, 
                    category: Optional[str] = None) -> bool:
        """Update task properties."""
        for task in self.tasks:
            if task['id'] == task_id:
                if description:
                    task['description'] = description
                if priority:
                    task['priority'] = priority
                if category:
                    task['category'] = category
                self._save_tasks()
                return True
        return False
    
    def clear_completed(self) -> int:
        """Clear all completed tasks."""
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t['status'] != 'completed']
        self._save_tasks()
        return initial_count - len(self.tasks)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get task statistics."""
        total = len(self.tasks)
        if total == 0:
            return {
                'total': 0,
                'pending': 0,
                'completed': 0,
                'completion_rate': 0,
                'by_priority': {},
                'by_category': {}
            }
        
        pending = len([t for t in self.tasks if t['status'] == 'pending'])
        completed = total - pending
        
        # Count by priority
        by_priority = {}
        for priority in ['low', 'medium', 'high']:
            count = len([t for t in self.tasks if t['priority'] == priority])
            if count > 0:
                by_priority[priority] = count
        
        # Count by category
        by_category = {}
        for task in self.tasks:
            category = task['category']
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            'total': total,
            'pending': pending,
            'completed': completed,
            'completion_rate': round((completed / total) * 100, 1),
            'by_priority': by_priority,
            'by_category': by_category
        }
    
    def display_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Display tasks in a formatted table."""
        if not tasks:
            print("No tasks to display.")
            return
        
        # Print header
        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'Status':<12} {'Priority':<10} {'Category':<15} {'Description':<30}")
        print("=" * 80)
        
        # Print tasks
        for task in tasks:
            status_symbol = "[X]" if task['status'] == 'completed' else "[ ]"
            priority_symbol = self._get_priority_symbol(task['priority'])
            description = task['description'][:30] + '...' if len(task['description']) > 30 else task['description']
            
            print(f"{task['id']:<5} {status_symbol:<12} {priority_symbol:<10} "
                  f"{task['category']:<15} {description:<30}")
        
        print("=" * 80)
        print(f"Total: {len(tasks)} task(s)\n")
    
    def display_statistics(self, stats: Dict[str, Any]) -> None:
        """Display task statistics."""
        print("\n" + "=" * 50)
        print("TASK STATISTICS")
        print("=" * 50)
        
        print(f"Total tasks:      {stats['total']}")
        print(f"Pending tasks:    {stats['pending']}")
        print(f"Completed tasks:  {stats['completed']}")
        print(f"Completion rate:  {stats['completion_rate']}%")
        
        if stats['by_priority']:
            print("\nBy Priority:")
            for priority, count in stats['by_priority'].items():
                print(f"  {priority.capitalize():<10} {count}")
        
        if stats['by_category']:
            print("\nBy Category:")
            for category, count in sorted(stats['by_category'].items()):
                print(f"  {category:<15} {count}")
        
        print("=" * 50 + "\n")
    
    def _get_priority_symbol(self, priority: str) -> str:
        """Get a visual symbol for priority level."""
        symbols = {
            'low': '🟢 Low',
            'medium': '🟡 Med',
            'high': '🔴 HIGH!'
        }
        return symbols.get(priority, '⚪ Unknown')