#!/bin/bash

# Task Tracker - Full Stack Startup Script
# This script starts both the backend API and frontend development server

echo "Starting Task Tracker Full Stack Application..."
echo "================================================"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap for cleanup on script exit
trap cleanup EXIT INT TERM

# Start Backend API
echo "Starting Backend API on port 5001..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Error: Backend failed to start!"
    exit 1
fi

echo "Backend API is running at http://localhost:5001"
echo ""

# Start Frontend
echo "Starting Frontend Development Server on port 3000..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "================================================"
echo "Task Tracker is starting up!"
echo ""
echo "Backend API:  http://localhost:5001"
echo "Frontend App: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================"

# Wait for processes
wait