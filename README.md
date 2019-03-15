# Task Tracker CLI

A simple command-line task management tool written in Python with JSON storage.

## Features

- Add tasks with priority levels and categories
- List tasks with flexible filtering options
- Mark tasks as completed
- Update task details
- Delete tasks
- View task statistics
- Clear completed tasks
- Persistent storage using JSON

## Installation

This project requires Python 3.6 or higher.

```bash
# Clone the repository
git clone <repository-url>
cd task-tracker-cli

# Install development dependencies (optional)
pip install -r requirements.txt
```

## Usage

### Add a task
```bash
python main.py add "Complete project documentation"
python main.py add "Review pull request" -p high -c work
python main.py add "Buy groceries" -p low -c personal
```

### List tasks
```bash
# List all tasks
python main.py list

# List only pending tasks
python main.py list -s pending

# List tasks by category
python main.py list -c work

# List high priority tasks
python main.py list -p high
```

### Complete a task
```bash
python main.py complete 1
```

### Update a task
```bash
python main.py update 1 -d "Updated description"
python main.py update 1 -p high -c urgent
```

### Delete a task
```bash
python main.py delete 1
```

### View statistics
```bash
python main.py stats
```

### Clear completed tasks
```bash
python main.py clear
python main.py clear -f  # Skip confirmation
```

## Task Properties

- **ID**: Unique identifier for each task
- **Description**: Task description text
- **Priority**: low, medium (default), or high
- **Category**: Task category (default: general)
- **Status**: pending or completed
- **Created At**: Timestamp when task was created
- **Completed At**: Timestamp when task was completed

## Data Storage

Tasks are stored in a `tasks.json` file in the current directory. The file is automatically created when you add your first task.

## Testing

Run the test suite:
```bash
python -m pytest
python -m pytest -v  # Verbose output
python -m pytest --cov=.  # With coverage
```

## License

MIT License

## Author

Kenneth Feh (2019)