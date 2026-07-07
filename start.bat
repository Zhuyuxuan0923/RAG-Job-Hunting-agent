@echo off
chcp 65001 > nul
title Agentic RAG 求职助手 - 本地启动

echo.
echo ╔══════════════════════════════════════════════╗
echo ║     Agentic RAG 求职助手 — 一键启动          ║
echo ╚══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:: ===== 检查后端依赖 =====
echo [1/4] 检查后端依赖...
if not exist "backend\.venv" (
    echo   ⚠ 未找到虚拟环境，正在安装依赖...
    cd backend
    poetry install --no-dev
    cd ..
) else (
    echo   ✓ 后端依赖已就绪
)

:: ===== 检查前端依赖 =====
echo [2/4] 检查前端依赖...
if not exist "frontend\node_modules" (
    echo   ⚠ 未找到 node_modules，正在安装依赖...
    cd frontend
    call npm install
    cd ..
) else (
    echo   ✓ 前端依赖已就绪
)

:: ===== 启动后端 =====
echo [3/4] 启动后端服务 (端口 8000)...
cd backend
start "RAG-Backend" cmd /c "poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000"
cd ..

:: 等后端启动
timeout /t 3 /nobreak > nul

:: ===== 启动前端 =====
echo [4/4] 启动前端服务 (端口 5173)...
cd frontend
start "RAG-Frontend" cmd /c "npm run dev"
cd ..

echo.
echo ╔══════════════════════════════════════════════╗
echo ║  ✓ 启动完成！                               ║
echo ║                                            ║
echo ║  前端: http://localhost:5173                ║
echo ║  后端: http://localhost:8000/docs           ║
echo ║                                            ║
echo ║  关闭此窗口不会停止服务                     ║
echo ║  停止请关闭 RAG-Backend 和 RAG-Frontend     ║
echo ╚══════════════════════════════════════════════╝
echo.

pause
