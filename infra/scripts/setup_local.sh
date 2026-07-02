#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
docker compose up --build -d
sleep 8
docker compose exec backend python -m app.db.seed || true

echo "CogniWatch local stack is ready."
