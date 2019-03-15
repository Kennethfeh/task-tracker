"""
Unit tests for the TaskManager class.
"""

import json
import os
import pytest
from datetime import datetime
from task_manager import TaskManager


class TestTaskManager:
    """Test suite for TaskManager class."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create a TaskManager instance with a temporary data file."""
        data_file = tmp_path / "test_tasks.json"
        return TaskManager(str(data_file))
    
    def test_initialize_empty(self, manager):
        """Test initialization with no existing data file."""
        assert manager.tasks == []
    
    def test_add_task(self, manager):
        """Test adding a new task."""
        task_id = manager.add_task("Test task", priority="high", category="work")
        assert task_id == 1
        assert len(manager.tasks) == 1
        
        task = manager.tasks[0]
        assert task['description'] == "Test task"
        assert task['priority'] == "high"
        assert task['category'] == "work"
        assert task['status'] == "pending"
        assert task['completed_at'] is None
    
    def test_add_multiple_tasks(self, manager):
        """Test adding multiple tasks with incrementing IDs."""
        id1 = manager.add_task("Task 1")
        id2 = manager.add_task("Task 2")
        id3 = manager.add_task("Task 3")
        
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        assert len(manager.tasks) == 3
    
    def test_list_all_tasks(self, manager):
        """Test listing all tasks."""
        manager.add_task("Task 1", priority="low")
        manager.add_task("Task 2", priority="high")
        manager.add_task("Task 3", priority="medium")
        
        tasks = manager.list_tasks()
        assert len(tasks) == 3
    
    def test_list_tasks_by_status(self, manager):
        """Test filtering tasks by status."""
        id1 = manager.add_task("Pending task")
        id2 = manager.add_task("Completed task")
        manager.complete_task(id2)
        
        pending = manager.list_tasks(status="pending")
        assert len(pending) == 1
        assert pending[0]['id'] == id1
        
        completed = manager.list_tasks(status="completed")
        assert len(completed) == 1
        assert completed[0]['id'] == id2
    
    def test_list_tasks_by_category(self, manager):
        """Test filtering tasks by category."""
        manager.add_task("Work task", category="work")
        manager.add_task("Personal task", category="personal")
        manager.add_task("Another work task", category="work")
        
        work_tasks = manager.list_tasks(category="work")
        assert len(work_tasks) == 2
        
        personal_tasks = manager.list_tasks(category="personal")
        assert len(personal_tasks) == 1
    
    def test_list_tasks_by_priority(self, manager):
        """Test filtering tasks by priority."""
        manager.add_task("Low priority", priority="low")
        manager.add_task("High priority 1", priority="high")
        manager.add_task("High priority 2", priority="high")
        
        high_priority = manager.list_tasks(priority="high")
        assert len(high_priority) == 2
        
        low_priority = manager.list_tasks(priority="low")
        assert len(low_priority) == 1
    
    def test_complete_task(self, manager):
        """Test marking a task as completed."""
        task_id = manager.add_task("Task to complete")
        
        result = manager.complete_task(task_id)
        assert result is True
        
        task = manager.tasks[0]
        assert task['status'] == "completed"
        assert task['completed_at'] is not None
    
    def test_complete_nonexistent_task(self, manager):
        """Test completing a task that doesn't exist."""
        result = manager.complete_task(999)
        assert result is False
    
    def test_delete_task(self, manager):
        """Test deleting a task."""
        task_id = manager.add_task("Task to delete")
        assert len(manager.tasks) == 1
        
        result = manager.delete_task(task_id)
        assert result is True
        assert len(manager.tasks) == 0
    
    def test_delete_nonexistent_task(self, manager):
        """Test deleting a task that doesn't exist."""
        result = manager.delete_task(999)
        assert result is False
    
    def test_update_task(self, manager):
        """Test updating task properties."""
        task_id = manager.add_task("Original", priority="low", category="work")
        
        result = manager.update_task(
            task_id,
            description="Updated",
            priority="high",
            category="personal"
        )
        assert result is True
        
        task = manager.tasks[0]
        assert task['description'] == "Updated"
        assert task['priority'] == "high"
        assert task['category'] == "personal"
    
    def test_update_nonexistent_task(self, manager):
        """Test updating a task that doesn't exist."""
        result = manager.update_task(999, description="New")
        assert result is False
    
    def test_clear_completed(self, manager):
        """Test clearing completed tasks."""
        id1 = manager.add_task("Pending task")
        id2 = manager.add_task("Completed task 1")
        id3 = manager.add_task("Completed task 2")
        
        manager.complete_task(id2)
        manager.complete_task(id3)
        
        count = manager.clear_completed()
        assert count == 2
        assert len(manager.tasks) == 1
        assert manager.tasks[0]['id'] == id1
    
    def test_get_statistics(self, manager):
        """Test getting task statistics."""
        # Add tasks with different properties
        manager.add_task("Task 1", priority="high", category="work")
        manager.add_task("Task 2", priority="high", category="work")
        manager.add_task("Task 3", priority="low", category="personal")
        id4 = manager.add_task("Task 4", priority="medium", category="personal")
        
        manager.complete_task(id4)
        
        stats = manager.get_statistics()
        
        assert stats['total'] == 4
        assert stats['pending'] == 3
        assert stats['completed'] == 1
        assert stats['completion_rate'] == 25.0
        assert stats['by_priority']['high'] == 2
        assert stats['by_priority']['low'] == 1
        assert stats['by_priority']['medium'] == 1
        assert stats['by_category']['work'] == 2
        assert stats['by_category']['personal'] == 2
    
    def test_get_statistics_empty(self, manager):
        """Test statistics with no tasks."""
        stats = manager.get_statistics()
        
        assert stats['total'] == 0
        assert stats['pending'] == 0
        assert stats['completed'] == 0
        assert stats['completion_rate'] == 0
        assert stats['by_priority'] == {}
        assert stats['by_category'] == {}
    
    def test_persistence(self, tmp_path):
        """Test that tasks persist between manager instances."""
        data_file = tmp_path / "persist_tasks.json"
        
        # Create first manager and add tasks
        manager1 = TaskManager(str(data_file))
        id1 = manager1.add_task("Persistent task 1")
        id2 = manager1.add_task("Persistent task 2")
        manager1.complete_task(id2)
        
        # Create second manager with same file
        manager2 = TaskManager(str(data_file))
        
        assert len(manager2.tasks) == 2
        assert manager2.tasks[0]['description'] == "Persistent task 1"
        assert manager2.tasks[1]['status'] == "completed"