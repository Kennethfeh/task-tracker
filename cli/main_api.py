#!/usr/bin/env python3
"""
Task Tracker CLI - API-enabled version
Author: Kenneth Feh
Created: 2019
"""

import argparse
import sys
from api_client import TaskAPIClient
from task_manager import TaskManager


def get_client(use_api=True):
    """Get appropriate client based on API availability."""
    if use_api:
        client = TaskAPIClient()
        if client.check_connection():
            return client, True
        else:
            print("Warning: API not available, falling back to local mode")
    
    # Fall back to local task manager
    return TaskManager(), False


def display_tasks(tasks):
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
        priority_symbol = f"({task['priority'].upper()[:3]})"
        description = task['description'][:30] + '...' if len(task['description']) > 30 else task['description']
        
        print(f"{task['id']:<5} {status_symbol:<12} {priority_symbol:<10} "
              f"{task['category']:<15} {description:<30}")
    
    print("=" * 80)
    print(f"Total: {len(tasks)} task(s)\n")


def display_statistics(stats):
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


def main():
    """Main entry point for the Task Tracker CLI."""
    parser = argparse.ArgumentParser(
        description='Task Tracker CLI - Manage your tasks from the command line',
        epilog='Example: python main_api.py add "Complete project documentation"'
    )
    
    parser.add_argument('--local', action='store_true', 
                       help='Use local storage instead of API')
    
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
    
    # Get appropriate client
    client, is_api = get_client(use_api=not args.local)
    mode = "API" if is_api else "Local"
    
    if args.command:
        print(f"[{mode} Mode]", end=" ")
    
    try:
        if args.command == 'add':
            task_id = client.add_task(
                args.description,
                priority=args.priority,
                category=args.category
            )
            print(f"Task added successfully! (ID: {task_id})")
            
        elif args.command == 'list':
            tasks = client.list_tasks(
                status=args.status,
                category=args.category,
                priority=args.priority
            )
            
            if is_api:
                display_tasks(tasks)
            else:
                client.display_tasks(tasks)
                
        elif args.command == 'complete':
            if client.complete_task(args.task_id):
                print(f"Task {args.task_id} marked as completed!")
            else:
                print(f"Error: Task {args.task_id} not found.")
                sys.exit(1)
                
        elif args.command == 'delete':
            if client.delete_task(args.task_id):
                print(f"Task {args.task_id} deleted successfully!")
            else:
                print(f"Error: Task {args.task_id} not found.")
                sys.exit(1)
                
        elif args.command == 'update':
            if not any([args.description, args.priority, args.category]):
                print("Error: At least one field must be specified for update.")
                sys.exit(1)
                
            if client.update_task(
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
            stats = client.get_statistics()
            if is_api:
                display_statistics(stats)
            else:
                client.display_statistics(stats)
            
        elif args.command == 'clear':
            if not args.force:
                response = input("Are you sure you want to clear all completed tasks? (y/n): ")
                if response.lower() != 'y':
                    print("Operation cancelled.")
                    return
                    
            count = client.clear_completed()
            print(f"Cleared {count} completed task(s).")
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()