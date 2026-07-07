@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo ==============================================
echo   Agentic RAG Job Assistant - Quick Start
echo ==============================================
echo.

:: ===== Check Backend =====
echo [1/4] Checking backend dependencies...
if not exist "backend\.venv" (
    echo   [WARN] .venv not found, running poetry install...
    cd backend
    poetry install --no-dev
    cd ..
) else (
    echo   [OK] Backend deps ready
)

:: ===== Check Frontend =====
echo [2/4] Checking frontend dependencies...
if not exist "frontend\node_modules" (
    echo   [WARN] node_modules not found, running npm install...
    cd frontend
    call npm install
    cd ..
) else (
    echo   [OK] Frontend deps ready
)

:: ===== Start Backend =====
echo [3/4] Starting backend on port 8000...
cd backend
start "RAG-Backend" cmd /k "poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000"
cd ..

:: Wait for backend to start
ping -n 4 127.0.0.1 >nul

:: ===== Start Frontend =====
echo [4/4] Starting frontend on port 5173...
cd frontend
start "RAG-Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ==============================================
echo   [DONE] Both services started!
echo.
echo   Frontend : http://localhost:5173
echo   Backend  : http://localhost:8000/docs
echo.
echo   Close the cmd windows to stop services.
echo ==============================================
echo.

pause
