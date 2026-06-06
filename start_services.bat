@echo off
echo ==================================================
echo   Starting Aegis Intelligence Gateway (Local)
echo ==================================================

cd /d "%~dp0"

if not exist venv (
    echo Creating python virtual environment (venv)...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/verifying dependencies...
pip install --upgrade pip
pip install fastapi uvicorn pydantic python-multipart httpx

echo Launching unified gateway on port 8080...
python main.py

pause
