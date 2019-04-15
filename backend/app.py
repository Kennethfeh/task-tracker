#!/usr/bin/env python3
"""
Task Tracker Backend API - RESTful API for task management
Author: Kenneth Feh
Created: 2019
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Add parent directory to path to import TaskManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli.task_manager import TaskManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the absolute path for data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'tasks.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize task manager with a backend-specific data file
task_manager = TaskManager(data_file=DATA_FILE)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'task-tracker-api'}), 200


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filters."""
    try:
        status = request.args.get('status', 'all')
        category = request.args.get('category')
        priority = request.args.get('priority')
        
        tasks = task_manager.list_tasks(
            status=status,
            category=category,
            priority=priority
        )
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                'success': False,
                'error': 'Description is required'
            }), 400
        
        task_id = task_manager.add_task(
            description=data['description'],
            priority=data.get('priority', 'medium'),
            category=data.get('category', 'general')
        )
        
        # Get the created task
        tasks = task_manager.list_tasks()
        created_task = next((t for t in tasks if t['id'] == task_id), None)
        
        return jsonify({
            'success': True,
            'task': created_task,
            'message': f'Task created with ID {task_id}'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No update data provided'
            }), 400
        
        success = task_manager.update_task(
            task_id=task_id,
            description=data.get('description'),
            priority=data.get('priority'),
            category=data.get('category')
        )
        
        if success:
            # Get the updated task
            tasks = task_manager.list_tasks()
            updated_task = next((t for t in tasks if t['id'] == task_id), None)
            
            return jsonify({
                'success': True,
                'task': updated_task,
                'message': f'Task {task_id} updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Task {task_id} not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed."""
    try:
        success = task_manager.complete_task(task_id)
        
        if success:
            # Get the completed task
            tasks = task_manager.list_tasks()
            completed_task = next((t for t in tasks if t['id'] == task_id), None)
            
            return jsonify({
                'success': True,
                'task': completed_task,
                'message': f'Task {task_id} marked as completed'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Task {task_id} not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        success = task_manager.delete_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Task {task_id} deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Task {task_id} not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks/clear-completed', methods=['POST'])
def clear_completed_tasks():
    """Clear all completed tasks."""
    try:
        count = task_manager.clear_completed()
        
        return jsonify({
            'success': True,
            'count': count,
            'message': f'Cleared {count} completed task(s)'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get task statistics."""
    try:
        stats = task_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5001)