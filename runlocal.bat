@echo off
echo Starting Hardscapes Backend and Frontend...
start "Hardscapes Backend" cmd /k "cd /d c:\Users\johnm\ccode\hardscapes_back && .venv\Scripts\activate && uvicorn api:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul
start "Hardscapes Frontend" cmd /k "cd /d c:\Users\johnm\ccode\hardscapes_front && npm run dev"
echo.
echo Backend starting at http://localhost:8000
echo Frontend starting at http://localhost:5173
echo.
echo Close the spawned command windows to stop the servers.
pause
