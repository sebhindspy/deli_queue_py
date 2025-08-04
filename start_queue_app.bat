@echo off
REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Start FastAPI server in a new terminal window
start cmd /k "python -m uvicorn main:app --reload"

REM Wait a few seconds for the server to start
timeout /t 5 /nobreak >nul

REM Open web apps in default browser
start http://127.0.0.1:8000/guest
start http://127.0.0.1:8000/attendant
start http://127.0.0.1:8000/admin
