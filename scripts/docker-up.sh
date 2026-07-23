#!/usr/bin/env bash
# 文档用途：启动Docker Compose开发环境
# 文档内容：构建并启动后端、Web；仅自建对象存储时启动 MinIO
# 内容来源：AI自动生成，项目团队确认
# 更新方式：compose服务变化时更新
# 备注：执行前请确保已安装Docker和Docker Compose

set -euo pipefail

OBJECT_STORAGE_PROVIDER="${OBJECT_STORAGE_PROVIDER:-}"
if [[ -z "${OBJECT_STORAGE_PROVIDER}" && -f ".env" ]]; then
  OBJECT_STORAGE_PROVIDER="$(grep -E '^OBJECT_STORAGE_PROVIDER=' .env | tail -n 1 | cut -d= -f2- || true)"
fi
OBJECT_STORAGE_PROVIDER="${OBJECT_STORAGE_PROVIDER:-minio}"

HOST_PORT_WEB="${HOST_PORT_WEB:-}"
HOST_PORT_BACKEND="${HOST_PORT_BACKEND:-}"
HOST_PORT_MINIO_CONSOLE="${HOST_PORT_MINIO_CONSOLE:-}"
if [[ -f ".env" ]]; then
  HOST_PORT_WEB="${HOST_PORT_WEB:-$(grep -E '^HOST_PORT_WEB=' .env | tail -n 1 | cut -d= -f2- || true)}"
  HOST_PORT_BACKEND="${HOST_PORT_BACKEND:-$(grep -E '^HOST_PORT_BACKEND=' .env | tail -n 1 | cut -d= -f2- || true)}"
  HOST_PORT_MINIO_CONSOLE="${HOST_PORT_MINIO_CONSOLE:-$(grep -E '^HOST_PORT_MINIO_CONSOLE=' .env | tail -n 1 | cut -d= -f2- || true)}"
fi
HOST_PORT_WEB="${HOST_PORT_WEB:-3000}"
HOST_PORT_BACKEND="${HOST_PORT_BACKEND:-8000}"
HOST_PORT_MINIO_CONSOLE="${HOST_PORT_MINIO_CONSOLE:-9001}"

if [[ "${OBJECT_STORAGE_PROVIDER}" == "minio" || "${OBJECT_STORAGE_PROVIDER}" == "self-hosted-minio" ]]; then
  docker compose --profile self-hosted-storage up -d --build
  MINIO_STARTED=true
else
  docker compose up -d --build
  MINIO_STARTED=false
fi

echo "服务已启动："
echo "- Web: http://localhost:${HOST_PORT_WEB}"
echo "- Backend API: http://localhost:${HOST_PORT_BACKEND}/docs"
if [[ "${MINIO_STARTED}" == "true" ]]; then
  echo "- MinIO Console: http://localhost:${HOST_PORT_MINIO_CONSOLE}"
else
  echo "- Object Storage: ${OBJECT_STORAGE_PROVIDER}（未启动本地 MinIO）"
fi
