@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo     Free Video Transcriber (Windows Setup)
echo ===================================================

:: Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please download it from https://www.python.org/downloads/
    pause
    exit /b
)

:: Check for FFmpeg
ffmpeg -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARNING] FFmpeg is not installed or not in PATH.
    echo Whisper requires FFmpeg to extract audio.
    echo Please install FFmpeg: https://ffmpeg.org/download.html
    echo Or install it via winget: winget install ffmpeg
    pause
)

:: Create Virtual Environment if it doesnt exist
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

:: Activate Virtual Environment
call venv\Scripts\activate.bat

:: Install Requirements
echo [INFO] Installing required packages...
pip install -q -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b
)

:MENU
echo.
echo ===================================================
echo     How would you like to run the Transcriber?
echo ===================================================
echo 1. Local Desktop App (Tkinter) - Recommended for Windows
echo 2. Web App (Gradio) - Open in Browser
echo 3. Web App (Streamlit) - Open in Browser
echo 4. Command Line Interface (CLI)
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting Desktop App...
    python app_tkinter.py
    goto MENU
)
if "%choice%"=="2" (
    echo Starting Gradio Web App...
    python app_gradio.py
    goto MENU
)
if "%choice%"=="3" (
    echo Starting Streamlit Web App...
    streamlit run app.py
    goto MENU
)
if "%choice%"=="4" (
    echo.
    set /p url="Enter the Video URL: "
    set /p model="Enter model size (tiny/base/small/medium/large) [default: base]: "
    if "!model!"=="" set model=base
    python cli.py "!url!" -m !model!
    pause
    goto MENU
)
if "%choice%"=="5" (
    echo Exiting...
    exit /b
)

echo Invalid choice. Please try again.
goto MENU
