#!/usr/bin/env python3
"""
Example usage script for Task Tracker CLI
Demonstrates various features of the task management system.
"""

import subprocess
import sys


def run_command(cmd):
    """Run a CLI command and print the result."""
    print(f"\n$ {cmd}")
    print("-" * 50)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)
    return result.returncode == 0


def main():
    """Demonstrate Task Tracker CLI features."""
    print("=" * 60)
    print("TASK TRACKER CLI - Example Usage")
    print("=" * 60)
    
    # Add some tasks
    print("\n1. Adding tasks with different priorities and categories:")
    run_command('python3 main.py add "Design database schema" -p high -c backend')
    run_command('python3 main.py add "Create API endpoints" -p high -c backend')
    run_command('python3 main.py add "Build user interface" -p medium -c frontend')
    run_command('python3 main.py add "Write documentation" -p low -c docs')
    run_command('python3 main.py add "Setup CI/CD pipeline" -p medium -c devops')
    
    # List all tasks
    print("\n2. Listing all tasks:")
    run_command('python3 main.py list')
    
    # Complete some tasks
    print("\n3. Marking tasks as completed:")
    run_command('python3 main.py complete 1')
    run_command('python3 main.py complete 3')
    
    # List by status
    print("\n4. Filtering tasks by status:")
    print("\nPending tasks only:")
    run_command('python3 main.py list -s pending')
    
    print("\nCompleted tasks only:")
    run_command('python3 main.py list -s completed')
    
    # Filter by category
    print("\n5. Filtering tasks by category:")
    run_command('python3 main.py list -c backend')
    
    # Filter by priority
    print("\n6. Filtering tasks by priority:")
    run_command('python3 main.py list -p high')
    
    # Update a task
    print("\n7. Updating task details:")
    run_command('python3 main.py update 2 -d "Create RESTful API endpoints" -p medium')
    
    # Show statistics
    print("\n8. Viewing task statistics:")
    run_command('python3 main.py stats')
    
    # Delete a task
    print("\n9. Deleting a task:")
    run_command('python3 main.py delete 5')
    
    # Clear completed tasks
    print("\n10. Clearing completed tasks:")
    run_command('python3 main.py clear -f')
    
    # Final list
    print("\n11. Final task list:")
    run_command('python3 main.py list')
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()