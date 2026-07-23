@echo off
title A1-WAVE Dashboard Quick Start
color 0B

echo.
echo ========================================
echo    A1-WAVE DASHBOARD - QUICK START
echo ========================================
echo.

REM Quick start - just launch the dashboard
echo [INFO] Starting A1-WAVE Dashboard...
echo [INFO] Dashboard will be available at: http://localhost:7865
echo [INFO] For external access, use your machine's IP address
echo [INFO] Use the Refresh Data button for manual updates
echo [INFO] Press Ctrl+C to stop
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please run start_a1wave.bat for full setup.
    pause
    exit /b 1
)

REM Install dependencies if needed
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

REM Create directories
if not exist "data" mkdir data
if not exist "exports" mkdir exports
if not exist "snapshots" mkdir snapshots
if not exist "logs" mkdir logs

REM Start dashboard
streamlit run dashboard.py --server.port 7865
