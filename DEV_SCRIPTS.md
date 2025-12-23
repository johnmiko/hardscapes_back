# Hardscapes Development Scripts

## Backend (hardscapes_back)

### First time setup:
```powershell
cd hardscapes_back
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python build_words.py
```

### Run backend server:
```powershell
cd hardscapes_back
.\.venv\Scripts\activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
- API docs at: http://localhost:8000/docs
- Words endpoint: http://localhost:8000/words?level=1

---

## Frontend (hardscapes_front)

### First time setup:
```powershell
cd hardscapes_front
npm install
```

### Run frontend dev server:
```powershell
cd hardscapes_front
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## Run Both (Parallel)

In PowerShell, you can run both servers in the background:

```powershell
# Terminal 1 - Backend
cd c:\Users\johnm\ccode\hardscapes_back
.\.venv\Scripts\activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd c:\Users\johnm\ccode\hardscapes_front
npm run dev
```

Or use the provided convenience scripts (see below).

---

## Quick Start Scripts

### Windows PowerShell script (runlocal.ps1):
```powershell
# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd c:\Users\johnm\ccode\hardscapes_back; .\.venv\Scripts\activate; uvicorn api:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Start frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd c:\Users\johnm\ccode\hardscapes_front; npm run dev"
```

### Windows Batch script (runlocal.bat):
```batch
@echo off
start "Hardscapes Backend" cmd /k "cd /d c:\Users\johnm\ccode\hardscapes_back && .venv\Scripts\activate && uvicorn api:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul
start "Hardscapes Frontend" cmd /k "cd /d c:\Users\johnm\ccode\hardscapes_front && npm run dev"
```

---

## Testing the Connection

1. Start backend server
2. Start frontend server
3. Open http://localhost:5173 in browser
4. Select different levels to see words
5. Check browser console for any errors

---

## Rebuilding Word Database

If you modify `data/cefr.csv`:

```powershell
cd hardscapes_back
.\.venv\Scripts\activate
python build_words.py
```

This regenerates `out/words_ranked.csv` and `out/words.db`.

---

## Deployment

### Backend (Render/Fly/Railway):
- Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
- Environment: Python 3.11+
- Build command: `pip install -r requirements.txt && python build_words.py`

### Frontend (Vercel/Netlify):
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_BASE_URL=https://your-backend.com`
