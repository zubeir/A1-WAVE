@echo off
title A1-WAVE Dashboard Agent
color 0A

echo.
echo ========================================
echo    A1-WAVE DASHBOARD - STARTUP SCRIPT
echo    Ride macro waves. Exit before they break.
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Display Python version
echo [INFO] Python version:
python --version
echo.

REM Check if we're in the right directory
if not exist "dashboard.py" (
    echo [ERROR] dashboard.py not found
    echo Please run this script from the A1-WAVE directory
    pause
    exit /b 1
)

REM Install dependencies if needed
echo [INFO] Checking dependencies...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "data" mkdir data
if not exist "exports" mkdir exports
if not exist "snapshots" mkdir snapshots
if not exist "logs" mkdir logs

:MENU
cls
echo.
echo ========================================
echo    A1-WAVE DASHBOARD - STARTUP MENU
echo ========================================
echo.
echo 1. Start Dashboard Only (Manual Refresh)
echo 2. Start Agent Mode (Auto-Refresh Every 2 Hours)
echo 3. Run Data Collection Once
echo 4. View Recent Logs
echo 5. Exit
echo.
echo ========================================
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto DASHBOARD_ONLY
if "%choice%"=="2" goto AGENT_MODE
if "%choice%"=="3" goto DATA_COLLECTION
if "%choice%"=="4" goto VIEW_LOGS
if "%choice%"=="5" goto EXIT
goto INVALID_CHOICE

:DASHBOARD_ONLY
echo.
echo [INFO] Starting A1-WAVE Dashboard...
echo [INFO] Dashboard will be available at: http://localhost:7865
echo [INFO] For external access, use your machine's IP address
echo [INFO] Press Ctrl+C to stop the dashboard
echo.
echo [NOTE] Use the Refresh Data button on the dashboard for manual updates
echo.
pause
streamlit run dashboard.py --server.port 7865
goto MENU

:AGENT_MODE
echo.
echo [INFO] Starting A1-WAVE Agent (Auto-Refresh Mode)...
echo [INFO] Dashboard will be available at: http://localhost:7865
echo [INFO] For external access, use your machine's IP address
echo [INFO] Data will refresh automatically every 2 hours
echo [INFO] Logs will be saved to logs\agent.log
echo [INFO] Press Ctrl+C to stop the agent
echo.
echo [NOTE] You can still use the Refresh Data button for immediate updates
echo.
pause
python agent.py
goto MENU

:DATA_COLLECTION
echo.
echo [INFO] Running data collection once...
echo.
python start_agent.py --collect
echo.
pause
goto MENU

:VIEW_LOGS
echo.
echo [INFO] Recent agent logs:
echo ========================================
if exist "logs\agent.log" (
    type logs\agent.log | more
) else (
    echo No log file found yet. Run the agent first.
)
echo.
pause
goto MENU

:INVALID_CHOICE
echo.
echo [ERROR] Invalid choice. Please enter 1-5.
pause
goto MENU

:EXIT
echo.
echo [INFO] Goodbye!
echo.
exit /b 0
