#!/bin/bash

# Swing Trading Assistant - Local Startup Script
# Usage: bash start.sh

set -e

echo "🚀 Swing Trading Assistant - Starting..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✏️  Please edit .env with your Telegram credentials and run again"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Run the application
echo "✅ Starting FastAPI server..."
echo "📍 API available at: http://localhost:10000"
echo "📖 Documentation at: http://localhost:10000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
