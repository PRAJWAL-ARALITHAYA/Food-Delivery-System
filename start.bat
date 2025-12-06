@echo off
REM Food Delivery System - Startup Script for Windows
REM This script helps you start the application quickly

echo.
echo ========================================
echo  Food Delivery System - Startup Helper
echo ========================================
echo.

:menu
echo.
echo Choose what you want to do:
echo.
echo 1. Setup Backend (install dependencies)
echo 2. Start Backend (Flask server)
echo 3. Setup Frontend (install dependencies)
echo 4. Start Frontend (React app)
echo 5. View Documentation
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto setup_backend
if "%choice%"=="2" goto start_backend
if "%choice%"=="3" goto setup_frontend
if "%choice%"=="4" goto start_frontend
if "%choice%"=="5" goto view_docs
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto menu

:setup_backend
echo.
echo Setting up Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Backend setup complete!
echo Next: Run "python app.py" to start the Flask server
cd ..
pause
goto menu

:start_backend
echo.
echo Starting Backend Flask Server...
echo.
cd backend
if not exist venv (
    echo Virtual environment not found. Running setup first...
    call :setup_backend
)
call venv\Scripts\activate.bat
echo.
echo Starting Flask on http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py
cd ..
goto menu

:setup_frontend
echo.
echo Setting up Frontend...
cd frontend
echo Checking if npm is installed...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: npm is not installed!
    echo Please install Node.js from https://nodejs.org/
    cd ..
    pause
    goto menu
)
echo Installing npm dependencies...
npm install
echo.
echo Frontend setup complete!
echo Next: Run "npm start" to start the React app
cd ..
pause
goto menu

:start_frontend
echo.
echo Starting Frontend React App...
echo.
cd frontend
echo Checking if npm is installed...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: npm is not installed!
    echo Please install Node.js from https://nodejs.org/
    cd ..
    pause
    goto menu
)
if not exist node_modules (
    echo Dependencies not found. Running setup first...
    call :setup_frontend
)
echo.
echo Starting React on http://localhost:3000
echo.
npm start
cd ..
goto menu

:view_docs
echo.
cls
echo ========================================
echo        FOOD DELIVERY SYSTEM DOCS
echo ========================================
echo.
echo 📖 Available Documentation:
echo.
echo    1. README.md - Complete documentation
echo    2. QUICKSTART.md - Quick setup guide
echo    3. SETUP.md - Environment configuration
echo    4. API_TESTING.md - API testing guide
echo    5. PROJECT_SUMMARY.md - Project details
echo.
echo Opening README.md...
echo.
if exist README.md (
    notepad README.md
) else (
    echo README.md not found!
)
pause
goto menu

:exit
echo.
echo Thank you for using Food Delivery System!
echo.
exit /b
