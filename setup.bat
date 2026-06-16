@echo off
REM FinSight Quick Start Script for Windows

echo ================================
echo   FinSight - Quick Start Setup   
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo [OK] Python and Node.js detected
echo.

REM Setup Python backend
echo Setting up Python Backend...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

echo [OK] Python backend ready
echo.

REM Setup Node frontend
echo Setting up React Frontend...
if not exist "node_modules" (
    echo Installing Node dependencies...
    npm install --quiet
) else (
    echo Node modules already installed
)

echo [OK] React frontend ready
echo.

REM Create .env file
echo Configuring environment...
if not exist ".env" (
    (
        echo # FinSight Environment Configuration
        echo REACT_APP_API_URL=http://localhost:8000
        echo DATABASE_URL=sqlite:///./finsight.db
        echo.
        echo # Optional: Add your Google API key for Gemini
        echo # GOOGLE_API_KEY=your-key-here
    ) > .env
    echo Created .env file
)

echo [OK] Environment configured
echo.

REM Summary
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the application:
echo.
echo   Option 1: Run everything (requires 3 terminals)
echo     Terminal 1: python backend.py
echo     Terminal 2: npm start
echo     Terminal 3: python seed_data.py (after backend/frontend start)
echo.
echo   Option 2: Using Docker (requires Docker ^& Docker Compose)
echo     docker-compose up
echo.
echo Then open http://localhost:3000 in your browser
echo.
echo First user credentials (after seed_data.py):
echo   Email: priya.sharma@college.com
echo   Amount: ₹15,000
echo.
echo [TIP] Set GOOGLE_API_KEY in .env for AI Coach feature
echo.

pause
