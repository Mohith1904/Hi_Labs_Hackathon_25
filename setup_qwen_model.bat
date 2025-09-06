@echo off
echo Setting up Qwen2.5 7B model for Provider Data Quality Analytics...
echo.

echo [1/2] Checking if Ollama is running...
ollama list
if %errorlevel% neq 0 (
    echo ❌ Ollama is not running. Please start Ollama first.
    echo Download from: https://ollama.ai/
    pause
    exit /b 1
)

echo.
echo [2/2] Pulling Qwen2.5 Coder 7B model...
echo This may take a few minutes depending on your internet connection...
ollama pull qwen2.5-coder:7b

echo.
echo ✅ Setup complete! Qwen2.5 Coder 7B model is ready to use.
echo.
echo You can now run your application with:
echo   python app.py
echo.
pause
