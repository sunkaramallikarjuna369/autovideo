@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   YOUTUBE FACELESS VIDEO GENERATOR - ONE CLICK AUTOMATION
echo ============================================================
echo.
echo   This tool will automatically:
echo   1. Set up a Python virtual environment
echo   2. Install all required packages
echo   3. Generate videos with AI scripts and stock footage
echo.
echo ============================================================
echo.

:: Step 1: Check Python
echo [STEP 1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo   ERROR: Python is not installed or not in PATH!
    echo   Please install Python 3.8+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo   Found Python %PYVER%
echo.

:: Set the script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Step 2: Virtual Environment
echo [STEP 2/4] Setting up virtual environment...
if not exist "venv" (
    echo   Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo   ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo   Virtual environment created!
) else (
    echo   Virtual environment already exists.
)
echo.

:: Activate virtual environment
echo [STEP 3/4] Activating virtual environment and installing packages...
call venv\Scripts\activate.bat
echo   Installing/updating packages (this may take a minute)...
python -m pip install --upgrade pip -q 2>nul
python -m pip install -r requirements.txt -q 2>nul
echo   Packages installed!
echo.

:: Step 4: Check .env file
echo [STEP 4/4] Checking API keys configuration...
if not exist ".env" (
    if exist ".env.example" (
        echo   Creating .env from template...
        copy ".env.example" ".env" >nul
        echo   .env file created!
    ) else (
        echo   ERROR: .env.example not found!
        pause
        exit /b 1
    )
)

:: Check if keys are placeholder values or real keys
findstr /C:"your_" ".env" >nul 2>&1
if errorlevel 1 (
    echo   API keys are configured!
    echo.
    echo ============================================================
    echo   SETUP COMPLETE! Ready to generate videos.
    echo ============================================================
    echo.
    timeout /t 2 >nul
    goto menu
) else (
    echo.
    echo ============================================================
    echo   API KEYS NEED TO BE CONFIGURED
    echo ============================================================
    echo.
    echo   The .env file contains placeholder values.
    echo   Please edit .env and add your API keys.
    echo.
    echo   Opening .env file in Notepad...
    echo.
    notepad ".env"
    echo.
    echo   After saving your API keys, run this script again.
    echo.
    pause
    exit /b 0
)

:: Main menu
:menu
cls
echo ============================================================
echo   YOUTUBE FACELESS VIDEO GENERATOR
echo ============================================================
echo.
echo   1. Generate Video (Enter topic manually)
echo   2. Show Trending Topics (Monetization Focused)
echo   3. Interactive Mode (Step-by-step prompts)
echo   4. Quick Generate (Use suggested topic)
echo   5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto manual
if "%choice%"=="2" goto trends
if "%choice%"=="3" goto interactive
if "%choice%"=="4" goto quick
if "%choice%"=="5" goto end
goto menu

:manual
echo.
set /p topic="Enter video topic: "
if "%topic%"=="" (
    echo ERROR: Topic cannot be empty!
    pause
    goto menu
)
set /p length="Enter video length in minutes (default: 8): "
if "%length%"=="" set length=8
set /p ai="Choose AI provider (auto/groq/gemini/ollama, default: auto): "
if "%ai%"=="" set ai=auto

echo.
echo ============================================================
echo   GENERATING VIDEO
echo ============================================================
echo   Topic: %topic%
echo   Length: %length% minutes
echo   AI Provider: %ai%
echo ============================================================
echo.

python autovideo.py --topic "%topic%" --length %length% --ai %ai%

echo.
echo ============================================================
echo   VIDEO GENERATION COMPLETE!
echo ============================================================
echo.
echo Your video files are in the projects folder.
echo.
pause
goto menu

:trends
echo.
echo ============================================================
echo   FETCHING TRENDING TOPICS...
echo ============================================================
echo.
python autovideo.py --suggest-topics
echo.
pause
goto menu

:interactive
echo.
python autovideo.py --interactive
echo.
pause
goto menu

:quick
echo.
echo ============================================================
echo   QUICK GENERATE - HIGH CPM TOPICS
echo ============================================================
echo.
echo Select a topic category:
echo   1. Finance (CPM: $15-$50)
echo   2. Technology (CPM: $10-$30)
echo   3. Business (CPM: $12-$35)
echo   4. Health (CPM: $10-$25)
echo   5. Education (CPM: $8-$20)
echo.
set /p cat="Enter category (1-5): "

if "%cat%"=="1" set topic=5 Investment Mistakes That Cost You Thousands
if "%cat%"=="2" set topic=AI Tools That Will Change Your Life
if "%cat%"=="3" set topic=Business Ideas You Can Start Today
if "%cat%"=="4" set topic=Morning Habits of Successful People
if "%cat%"=="5" set topic=Skills That Will Make You Rich

if "%topic%"=="" (
    echo Invalid selection!
    pause
    goto menu
)

echo.
echo Selected topic: %topic%
echo.
set /p confirm="Generate video with this topic? (y/n): "
if /i not "%confirm%"=="y" goto menu

echo.
echo ============================================================
echo   GENERATING VIDEO
echo ============================================================
echo   Topic: %topic%
echo   Length: 8 minutes
echo   AI Provider: auto
echo ============================================================
echo.

python autovideo.py --topic "%topic%" --length 8 --ai auto

echo.
echo ============================================================
echo   VIDEO GENERATION COMPLETE!
echo ============================================================
echo.
pause
goto menu

:end
echo.
echo Thank you for using YouTube Faceless Video Generator!
echo.
call venv\Scripts\deactivate.bat 2>nul
exit /b 0
