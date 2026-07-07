@echo off
cd /d "%~dp0"

if not exist .env (
    echo ERROR: .env file not found.
    echo Please copy .env.example to .env and fill in your API keys:
    echo   copy .env.example .env
    echo   notepad .env
    exit /b 1
)

echo === Building and starting services ===
docker compose up -d --build

echo.
echo === Services started! ===
echo   Frontend : http://localhost
echo   Backend  : http://localhost:8000
echo   API Docs : http://localhost:8000/docs
echo.
echo View logs:  docker compose logs -f
echo Stop:       docker compose down
