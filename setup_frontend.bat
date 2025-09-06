@echo off
echo Setting up Provider Data Quality Analytics Frontend...
echo.

echo Installing Node.js dependencies...
cd frontend
npm install

echo.
echo Frontend setup complete!
echo.
echo To start the frontend:
echo 1. Make sure your Flask backend is running on http://127.0.0.1:5001
echo 2. Run: cd frontend && npm start
echo 3. Open http://localhost:3000 in your browser
echo.
pause
