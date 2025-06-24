@echo off
echo Starting AI Music Genre Classifier development server...

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not installed. Installing requirements...
    pip install -r requirements.txt
)

REM Start the development server
echo Starting FastAPI development server...
echo Server will be available at: http://localhost:8000
echo API docs available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py