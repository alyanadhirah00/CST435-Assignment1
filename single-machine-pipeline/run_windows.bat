@echo off
echo ==========================================
echo      Java RMI Pipeline Launcher
echo ==========================================

:: 1. Cleanup old Java processes
echo [1/4] Cleaning up old Java processes...
taskkill /F /IM java.exe /T >nul 2>&1

:: 2. Compile
echo [2/4] Compiling Java files...
javac *.java
if %errorlevel% neq 0 (
    echo.
    echo !!!!!!! COMPILATION FAILED !!!!!!!
    pause
    exit /b
)

:: 3. Start Services
echo [3/4] Starting Services...
if not exist "reports" mkdir reports

:: Start Service A (Clean) - This starts Registry
start "Service A" cmd /k "java ServiceA"
timeout /t 2 >nul

start "Service B" cmd /k "java ServiceB"
start "Service C" cmd /k "java ServiceC"
start "Service D" cmd /k "java ServiceD"

echo Services launched. Waiting 3 seconds...
timeout /t 3 >nul

:: 4. Start Client
echo [4/4] Starting Client...
echo.
echo ================= CLIENT OUTPUT =================
java Client
echo =================================================
echo.
pause