@echo off
echo ========================================
echo Provider Data Quality Analytics
echo ========================================
echo.

echo Starting the application...
echo.

echo [1/4] Installing Python dependencies...
pip install pandas fastapi uvicorn phonenumbers fuzzywuzzy python-levenshtein vanna

echo.
echo [2/4] Setting up Qwen2.5 Coder 7B model...
ollama pull qwen2.5-coder:7b

echo.
echo [3/4] Starting Flask backend...
start "Backend Server" cmd /k "python app.py"

echo.
echo [4/4] Starting React frontend...
cd frontend
start "Frontend Server" cmd /k "npm install && npm start"

echo.
echo ========================================
echo Application is starting up!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:5001
echo Frontend: http://localhost:3000
echo.
echo Alternative (Simple HTML): Open frontend/simple/index.html
echo.
echo Press any key to exit...
pause > nul
