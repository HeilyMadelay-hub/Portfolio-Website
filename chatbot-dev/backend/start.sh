#!/bin/bash

echo "========================================"
echo "   HYBRID CHATBOT - QUICK START"
echo "========================================"
echo

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.11+ from https://www.python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${YELLOW}WARNING: Python $REQUIRED_VERSION+ is recommended. You have $PYTHON_VERSION${NC}"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! pip show flask &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo
    echo -e "${YELLOW}IMPORTANT: Please edit .env and add your Google Gemini API key${NC}"
    echo
    echo "Press Enter to continue..."
    read
fi

# Start the application
echo
echo -e "${GREEN}Starting the application...${NC}"
echo
echo -e "Chat API: ${GREEN}http://localhost:5000/api/chat${NC}"
echo -e "Dashboard: ${GREEN}http://localhost:5000/api/monitoring/dashboard${NC}"
echo

# Check if we should use FastAPI
if [ "$1" == "fastapi" ]; then
    USE_FASTAPI=true python3 main.py
else
    python3 main.py
fi
