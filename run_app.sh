#!/bin/bash

# Zfarming App Startup Script
echo "🌱 Starting Zfarming - Urban Garden Helper"
echo "=========================================="

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
pip install -r requirements.txt

# Run the application
echo "Starting Streamlit application..."
echo "The app will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
