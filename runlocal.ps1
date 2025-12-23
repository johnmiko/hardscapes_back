# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd c:\Users\johnm\ccode\hardscapes_back; .\.venv\Scripts\activate; uvicorn api:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Start frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd c:\Users\johnm\ccode\hardscapes_front; npm run dev"

Write-Host "Backend starting at http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend starting at http://localhost:5173" -ForegroundColor Green
Write-Host "Close the spawned PowerShell windows to stop the servers." -ForegroundColor Yellow
