#!/bin/bash

# SoundCloud Weekly Updater - Backend Startup Script

echo "Starting SoundCloud Weekly Updater Backend..."
echo "=============================================="
echo ""

# Check if we're in the correct directory
if [ ! -f "secrets.env" ]; then
    echo "Error: secrets.env not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

if [ ! -f "sc_token.json" ]; then
    echo "Error: sc_token.json not found!"
    echo "Please generate tokens using: python3 SC_Token.py"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --reload --port 8000
