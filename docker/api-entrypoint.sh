#!/usr/bin/env sh
set -e

cd /app
export PYTHONPATH=/app

echo "[api] waiting for postgres ${PG_HOST:-db}:${PG_PORT:-5432}..."
until nc -z "${PG_HOST:-db}" "${PG_PORT:-5432}"; do
  sleep 1
done

echo "[api] running migrations..."
alembic upgrade head

echo "[api] loading initial data..."
python commands/data_loader.py

echo "[api] starting server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8080
