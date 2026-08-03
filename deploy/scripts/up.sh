#!/usr/bin/env bash
# 文档用途：按部署域与环境 ID 启动 Docker Compose
# 文档内容：解析 env、Compose、profile，启动前执行安全校验
# 内容来源：REQ-0093 standardize-deployment-environment-matrix
# 更新方式：新增部署环境时同步更新 case 映射和 README

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOMAIN="${1:-local}"
ENVIRONMENT="${2:-sqlite-minio-managed}"
PROFILE=""
COMPOSE_PROFILES=()

case "${DOMAIN}:${ENVIRONMENT}" in
  local:sqlite-minio-managed)
    ENV_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-managed.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-managed.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILE="self-hosted-storage"
    COMPOSE_PROFILES=("self-hosted-storage" "docs-site")
    ;;
  local:sqlite-minio-external)
    ENV_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-external.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-external.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    COMPOSE_PROFILES=("docs-site")
    ;;
  local:sqlite-tencent-cos)
    ENV_FILE="${ROOT_DIR}/deploy/local/sqlite-tencent-cos.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/sqlite-tencent-cos.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    COMPOSE_PROFILES=("docs-site")
    ;;
  local:mysql-minio-managed)
    ENV_FILE="${ROOT_DIR}/deploy/local/mysql-minio-managed.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/mysql-minio-managed.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILE="self-hosted-storage"
    COMPOSE_PROFILES=("self-hosted-storage" "docs-site")
    ;;
  local:mysql-minio-external)
    ENV_FILE="${ROOT_DIR}/deploy/local/mysql-minio-external.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/mysql-minio-external.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    COMPOSE_PROFILES=("docs-site")
    ;;
  local:mysql-tencent-cos)
    ENV_FILE="${ROOT_DIR}/deploy/local/mysql-tencent-cos.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/mysql-tencent-cos.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    COMPOSE_PROFILES=("docs-site")
    ;;
  prod:mysql-tencent-cos)
    ENV_FILE="${ROOT_DIR}/deploy/prod/mysql-tencent-cos.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/prod/mysql-tencent-cos.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/prod/compose.tencent-cos.yml"
    COMPOSE_PROFILES=("docs-site")
    ;;
  *)
    echo "未知部署环境：${DOMAIN} ${ENVIRONMENT}" >&2
    echo "请查看 deploy/README.md 获取可用环境 ID。" >&2
    exit 2
    ;;
esac

if [[ ! -f "${ENV_FILE}" ]]; then
  ENV_FILE="${EXAMPLE_FILE}"
  echo "未找到真实 env，使用示例文件进行启动/校验：${ENV_FILE}"
  echo "需要真实部署时请复制为去掉 .example 的 env 文件并替换占位值。"
fi

VALIDATE_ARGS=(--domain "${DOMAIN}" --environment "${ENVIRONMENT}" --env-file "${ENV_FILE}")
if [[ -n "${PROFILE}" ]]; then
  VALIDATE_ARGS+=(--profile "${PROFILE}")
fi
python "${ROOT_DIR}/deploy/scripts/validate-env.py" "${VALIDATE_ARGS[@]}"

COMPOSE_ARGS=(--project-name tilesfst --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}")
for COMPOSE_PROFILE in "${COMPOSE_PROFILES[@]}"; do
  COMPOSE_ARGS=(--profile "${COMPOSE_PROFILE}" "${COMPOSE_ARGS[@]}")
done

export TILESFST_DEPLOY_ENV_FILE="${ENV_FILE}"
docker compose "${COMPOSE_ARGS[@]}" up -d --build

HOST_PORT_WEB="$(grep -E '^HOST_PORT_WEB=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_BACKEND="$(grep -E '^HOST_PORT_BACKEND=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_MINIO_CONSOLE="$(grep -E '^HOST_PORT_MINIO_CONSOLE=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_MINTLIFY_DOCS="$(grep -E '^HOST_PORT_MINTLIFY_DOCS=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_WEB="${HOST_PORT_WEB:-3000}"
HOST_PORT_BACKEND="${HOST_PORT_BACKEND:-8000}"
HOST_PORT_MINIO_CONSOLE="${HOST_PORT_MINIO_CONSOLE:-9001}"
HOST_PORT_MINTLIFY_DOCS="${HOST_PORT_MINTLIFY_DOCS:-3001}"

echo "服务已启动："
echo "- Environment: ${DOMAIN}-${ENVIRONMENT}"
echo "- Web: http://localhost:${HOST_PORT_WEB}"
echo "- Backend API: http://localhost:${HOST_PORT_BACKEND}/docs"
if [[ "${PROFILE}" == "self-hosted-storage" ]]; then
  echo "- MinIO Console: http://localhost:${HOST_PORT_MINIO_CONSOLE}"
else
  echo "- Object Storage: external provider（未启动本地 MinIO）"
fi
if [[ "${DOMAIN}" == "local" || "${DOMAIN}" == "prod" ]]; then
  echo "- Docs Site: http://localhost:${HOST_PORT_MINTLIFY_DOCS}"
fi
