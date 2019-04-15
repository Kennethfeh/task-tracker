#!/usr/bin/env python3
"""
Task Tracker CLI - A simple command-line task management tool
Author: Kenneth Feh
Created: 2019
"""

import argparse
import json
import os
import sys
from datetime import datetime
from task_manager import TaskManager


def main():
    """Main entry point for the Task Tracker CLI."""
    parser = argparse.ArgumentParser(
        description='Task Tracker CLI - Manage your tasks from the command line',
        epilog='Example: python main.py add "Complete project documentation"'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'], 
                           default='medium', help='Task priority (default: medium)')
    add_parser.add_argument('-c', '--category', default='general', 
                           help='Task category (default: general)')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('-s', '--status', choices=['pending', 'completed', 'all'],
                            default='all', help='Filter by status (default: all)')
    list_parser.add_argument('-c', '--category', help='Filter by category')
    list_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'],
                            help='Filter by priority')
    
    # Complete task command
    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('task_id', type=int, help='Task ID to complete')
    
    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task ID to delete')
    
    # Update task command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', type=int, help='Task ID to update')
    update_parser.add_argument('-d', '--description', help='New task description')
    update_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'],
                              help='New task priority')
    update_parser.add_argument('-c', '--category', help='New task category')
    
    # Statistics command
    stats_parser = subparsers.add_parser('stats', help='Show task statistics')
    
    # Clear completed tasks command
    clear_parser = subparsers.add_parser('clear', help='Clear all completed tasks')
    clear_parser.add_argument('-f', '--force', action='store_true',
                             help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        if args.command == 'add':
            task_id = task_manager.add_task(
                args.description,
                priority=args.priority,
                category=args.category
            )
            print(f"Task added successfully! (ID: {task_id})")
            
        elif args.command == 'list':
            tasks = task_manager.list_tasks(
                status=args.status,
                category=args.category,
                priority=args.priority
            )
            
            if not tasks:
                print("No tasks found.")
            else:
                task_manager.display_tasks(tasks)
                
        elif args.command == 'complete':
            if task_manager.complete_task(args.task_id):
                print(f"Task {args.task_id} marked as completed!")
            else:
                print(f"Error: Task {args.task_id} not found.")
                sys.exit(1)
                
        elif args.command == 'delete':
            if task_manager.delete_task(args.task_id):
                print(f"Task {args.task_id} deleted successfully!")
            else:
                print(f"Error: Task {args.task_id} not found.")
                sys.exit(1)
                
        elif args.command == 'update':
            if not any([args.description, args.priority, args.category]):
                print("Error: At least one field must be specified for update.")
                sys.exit(1)
                
            if task_manager.update_task(
                args.task_id,
                description=args.description,
                priority=args.priority,
                category=args.category
            ):
                print(f"Task {args.task_id} updated successfully!")
            else:
                print(f"Error: Task {args.task_id} not found.")
                sys.exit(1)
                
        elif args.command == 'stats':
            stats = task_manager.get_statistics()
            task_manager.display_statistics(stats)
            
        elif args.command == 'clear':
            if not args.force:
                response = input("Are you sure you want to clear all completed tasks? (y/n): ")
                if response.lower() != 'y':
                    print("Operation cancelled.")
                    return
                    
            count = task_manager.clear_completed()
            print(f"Cleared {count} completed task(s).")
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()