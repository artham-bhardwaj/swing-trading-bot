@echo off
REM Swing Trading Assistant - Windows Startup Script
REM Usage: start.bat

echo.
echo ========================
echo Swing Trading Assistant
echo ========================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env with your Telegram credentials and run again
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create logs directory
if not exist "logs" mkdir logs

REM Run the application
echo.
echo Starting FastAPI server...
echo API available at: http://localhost:10000
echo Documentation at: http://localhost:10000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
