#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Check for .env
if [ ! -f .env ]; then
  echo "ERROR: .env file not found."
  echo "Please copy .env.example to .env and fill in your API keys:"
  echo "  cp .env.example .env"
  echo "  vim .env"
  exit 1
fi

# Auto-detect version from git tag, fallback to "latest"
if [ -z "$TAG" ]; then
  TAG=$(git describe --tags --exact-match 2>/dev/null || echo "latest")
fi
echo "=== Deploying version: $TAG ==="

echo "=== Building and starting services ==="
TAG=$TAG docker compose up -d --build

echo ""
echo "=== Services started! ==="
echo "  Frontend : http://localhost"
echo "  Backend  : http://localhost:8000"
echo "  API Docs : http://localhost:8000/docs"
echo ""
echo "View logs:  docker compose logs -f"
echo "Stop:       docker compose down"
