#!/bin/bash

# SoundCloud Weekly Updater - Frontend Startup Script

echo "Starting SoundCloud Weekly Updater Frontend..."
echo "==============================================="
echo ""

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo ""
echo "Starting Vite development server..."
echo "Frontend will be available at: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the dev server
npm run dev
