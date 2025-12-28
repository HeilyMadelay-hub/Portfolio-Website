@echo off
echo ========================================
echo   HYBRID CHATBOT - QUICK START
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your Google Gemini API key
    echo.
    pause
)

REM Start the application
echo.
echo Starting the application...
echo.
echo Chat API: http://localhost:5000/api/chat
echo Dashboard: http://localhost:5000/api/monitoring/dashboard
echo.
python main.py

pause
