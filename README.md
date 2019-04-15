# Task Tracker

A full-stack task management application with CLI, REST API, and React frontend.

## Project Structure

```
task-tracker/
├── cli/          # Command-line interface
├── backend/      # Flask REST API server
├── frontend/     # React web application
└── data/         # JSON data storage
```

## Features

- **Multi-interface**: Access via CLI, REST API, or web interface
- **Task Management**: Create, read, update, and delete tasks
- **Priority Levels**: Assign low, medium, or high priority to tasks
- **Categories**: Organize tasks by custom categories
- **Filtering**: Filter tasks by status, priority, or category
- **Statistics**: View completion rates and task distribution
- **Persistent Storage**: JSON-based data persistence

## Quick Start

### Backend API

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5001`

### Frontend Web App

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The web app will open at `http://localhost:3000`

### CLI Tool

The CLI can work in two modes:

1. **API Mode** (default): Communicates with the backend API
   ```bash
   cd cli
   python main_api.py add "Complete project documentation"
   python main_api.py list
   ```

2. **Local Mode**: Uses local JSON storage directly
   ```bash
   cd cli
   python main.py add "Complete project documentation"
   python main.py list
   ```

## API Endpoints

### Tasks

- `GET /api/tasks` - List all tasks with optional filters
  - Query params: `status`, `priority`, `category`
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `POST /api/tasks/{id}/complete` - Mark task as completed
- `DELETE /api/tasks/{id}` - Delete a task
- `POST /api/tasks/clear-completed` - Clear all completed tasks

### Statistics

- `GET /api/statistics` - Get task statistics

### Health Check

- `GET /api/health` - Check API health status

## CLI Commands

```bash
# Add a new task
python main_api.py add "Task description" -p high -c work

# List tasks
python main_api.py list -s pending -p high

# Complete a task
python main_api.py complete 1

# Update a task
python main_api.py update 1 -d "Updated description" -p low

# Delete a task
python main_api.py delete 1

# View statistics
python main_api.py stats

# Clear completed tasks
python main_api.py clear
```

## Development

### Running Tests

For the CLI:
```bash
cd cli
python -m pytest
```

### Technology Stack

- **Backend**: Python 3.7+, Flask, Flask-CORS
- **Frontend**: React, Axios, React Icons
- **CLI**: Python with argparse
- **Storage**: JSON file-based persistence

## Configuration

### Backend Configuration

The backend server runs on port 5001 by default. Modify the `app.py` file to change the port or host.

### Frontend Configuration

The frontend expects the API at `http://localhost:5001`. To use a different API URL, set the `REACT_APP_API_URL` environment variable:

```bash
REACT_APP_API_URL=http://your-api-url npm start
```

## Project History

This project was initially created in 2019 as a Python CLI tool and has been enhanced to include a full-stack web application with REST API and React frontend.

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Author

Kenneth Feh - 2019