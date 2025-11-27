@echo off
title RMI Pipeline Orchestrator

echo ========================================================
echo        Java RMI Parallel Processing Project
echo ========================================================

REM --- 1. Check for textfile directory ---
if not exist "textfile" (
    echo [Setup] 'textfile' folder not found. Creating it...
    mkdir textfile
    echo This is a sample text file for testing. > textfile\sample1.txt
    echo I love using Java RMI it is great. > textfile\sample2.txt
    echo This result is terrible and bad. > textfile\sample3.txt
    echo [Setup] Created 3 dummy files in 'textfile'.
)

REM --- 2. Compile Java Files ---
echo [Build] Compiling Java source files...
javac *.java

if %errorlevel% neq 0 (
   
    echo [Error] Compilation Failed! Please check your code.
    pause
    exit /b
)

echo [Build] Compilation Successful.

REM --- 3. Start the Server (ServiceLauncher) in a NEW Window ---
echo [Run] Launching Services (Server) in a new window...
REM 'start' opens a new window. 'cmd /k' keeps that window open so you can see logs.
start "RMI Services Server" cmd /k "java ServiceLauncher"

REM --- 4. Run the Client in THIS Window ---
echo [Run] Launching Client...
echo.
java Client

echo.
echo ========================================================
echo [System] Pipeline finished.
echo [System] You may close the "RMI Services Server" window manually.
echo ========================================================
pause