#!/bin/bash

# Quick development startup script
# This activates the venv and starts the development server

echo "Starting AI Music Genre Classifier development server..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Dependencies not installed. Installing requirements..."
    pip install -r requirements.txt
fi

# Start the development server
echo "Starting FastAPI development server..."
echo "Server will be available at: http://localhost:8000"
echo "API docs available at: http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop the server"
echo

python main.py