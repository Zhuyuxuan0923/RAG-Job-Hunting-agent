#!/bin/bash
set -e

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     Agentic RAG 求职助手 — 一键启动          ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

cleanup() {
    echo ""
    echo "正在停止服务..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "已停止"
    exit 0
}
trap cleanup SIGINT SIGTERM

# ===== 检查后端依赖 =====
echo "[1/4] 检查后端依赖..."
if [ ! -d "backend/.venv" ]; then
    echo "  ⚠ 未找到虚拟环境，正在安装依赖..."
    cd backend && poetry install --no-dev && cd ..
else
    echo "  ✓ 后端依赖已就绪"
fi

# ===== 检查前端依赖 =====
echo "[2/4] 检查前端依赖..."
if [ ! -d "frontend/node_modules" ]; then
    echo "  ⚠ 未找到 node_modules，正在安装依赖..."
    cd frontend && npm install && cd ..
else
    echo "  ✓ 前端依赖已就绪"
fi

# ===== 启动后端 =====
echo "[3/4] 启动后端服务 (端口 8000)..."
cd backend
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

sleep 2

# ===== 启动前端 =====
echo "[4/4] 启动前端服务 (端口 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  ✓ 启动完成！                               ║"
echo "║                                            ║"
echo "║  前端: http://localhost:5173                ║"
echo "║  后端: http://localhost:8000/docs           ║"
echo "║                                            ║"
echo "║  按 Ctrl+C 停止所有服务                     ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

wait
