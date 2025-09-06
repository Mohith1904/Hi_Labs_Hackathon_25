@echo off
echo Adding all files to git (excluding node_modules and other ignored files)...
echo.

echo [1/3] Checking git status...
git status

echo.
echo [2/3] Adding all files...
git add .

echo.
echo [3/3] Checking what will be committed...
git status

echo.
echo ✅ All files added to git!
echo.
echo To commit, run: git commit -m "Your commit message"
echo To push, run: git push origin main
echo.
pause
