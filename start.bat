@echo off

:: Clear screen
cls

:: Check if Git is installed
where git >nul 2>nul
if errorlevel 1 (
    echo Git is not installed. Please install Git and try again.
    exit /b 1
)

:: Update repository from GitHub
echo Updating repository from GitHub...
git pull origin main
if errorlevel 1 (
    echo Failed to pull the latest changes from GitHub.
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not added to PATH. Please install Python and try again.
    exit /b 1
)

:: Define virtual environment directory
set VENV_DIR=venv

:: Create virtual environment if it doesn't exist
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
    
    echo Activating virtual environment and installing requirements...
    call %VENV_DIR%\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

:: Navigate to app directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%app"

:: Clear screen and start bot
cls
echo Starting chatbot...
start /B python "chatbot.py" > chatbot.log 2>&1

:: Pause for user to review
pause
