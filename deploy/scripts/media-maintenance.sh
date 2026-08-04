#!/usr/bin/env bash
# 文档用途：运行媒体维护任务
# 文档内容：封装 local/prod Compose 维护入口，默认 dry-run，apply 必须显式确认备份
# 内容来源：REQ-0097 add-prod-media-maintenance-jobs 验收返修
# 更新方式：新增媒体维护任务或部署环境时同步更新

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

usage() {
  cat <<'EOF'
用法：
  deploy/scripts/media-maintenance.sh <local|prod> <environment> <task> [task args...]

示例：
  deploy/scripts/media-maintenance.sh prod mysql-tencent-cos object-key-audit --limit 100
  deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100
  deploy/scripts/media-maintenance.sh prod mysql-tencent-cos formalize-pending-tile-images --limit 100
  deploy/scripts/media-maintenance.sh prod mysql-tencent-cos formalize-pending-tile-images --limit 100 --apply --confirm-backup

说明：
  - 默认 task 为 object-key-audit，只读 dry-run。
  - 写入任务必须显式传入 --apply --confirm-backup。
  - 执行 apply 前必须先完成 MySQL 与对象存储 bucket/prefix 备份。
  - 脚本只解析 env 文件路径，不输出 env 内容、数据库连接串或对象存储密钥。
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

DOMAIN="${1:-prod}"
ENVIRONMENT="${2:-mysql-tencent-cos}"
TASK="${3:-object-key-audit}"
shift_count=0
if [[ $# -gt 0 ]]; then
  shift_count=1
fi
if [[ $# -gt 1 ]]; then
  shift_count=2
fi
if [[ $# -gt 2 ]]; then
  shift_count=3
fi
shift "${shift_count}"

case "${DOMAIN}:${ENVIRONMENT}" in
  local:sqlite-minio-managed)
    ENV_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-managed.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-managed.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILES=(--profile self-hosted-storage)
    SERVICE="tilesfst-backend"
    ;;
  local:sqlite-minio-external)
    ENV_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-external.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/sqlite-minio-external.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILES=()
    SERVICE="tilesfst-backend"
    ;;
  local:sqlite-tencent-cos)
    ENV_FILE="${ROOT_DIR}/deploy/local/sqlite-tencent-cos.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/sqlite-tencent-cos.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILES=()
    SERVICE="tilesfst-backend"
    ;;
  local:mysql-minio-managed)
    ENV_FILE="${ROOT_DIR}/deploy/local/mysql-minio-managed.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/mysql-minio-managed.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILES=(--profile self-hosted-storage)
    SERVICE="tilesfst-backend"
    ;;
  local:mysql-minio-external)
    ENV_FILE="${ROOT_DIR}/deploy/local/mysql-minio-external.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/mysql-minio-external.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILES=()
    SERVICE="tilesfst-backend"
    ;;
  local:mysql-tencent-cos)
    ENV_FILE="${ROOT_DIR}/deploy/local/mysql-tencent-cos.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/mysql-tencent-cos.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/local/compose.yml"
    PROFILES=()
    SERVICE="tilesfst-backend"
    ;;
  prod:mysql-tencent-cos)
    ENV_FILE="${ROOT_DIR}/deploy/prod/mysql-tencent-cos.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/prod/mysql-tencent-cos.env.example"
    COMPOSE_FILE="${ROOT_DIR}/deploy/prod/compose.tencent-cos.yml"
    PROFILES=(--profile maintenance)
    SERVICE="tilesfst-maintenance"
    ;;
  *)
    echo "未知部署环境：${DOMAIN} ${ENVIRONMENT}" >&2
    echo "用法：deploy/scripts/media-maintenance.sh <local|prod> <environment> <task> [--limit N] [--apply --confirm-backup]" >&2
    exit 2
    ;;
esac

if [[ ! -f "${ENV_FILE}" ]]; then
  ENV_FILE="${EXAMPLE_FILE}"
  echo "未找到真实 env，使用示例文件进行 dry-run/校验：${ENV_FILE}"
  echo "真实维护任务必须使用已替换占位值的 env 文件。"
fi

if [[ " $* " == *" --apply "* && " $* " != *" --confirm-backup "* ]]; then
  echo "写入维护任务必须同时传入 --confirm-backup，并先完成 MySQL 与对象存储 bucket/prefix 备份。" >&2
  exit 2
fi

DOCKER_COMPOSE_ARGS=()
if [[ ${#PROFILES[@]} -gt 0 ]]; then
  DOCKER_COMPOSE_ARGS+=("${PROFILES[@]}")
fi
DOCKER_COMPOSE_ARGS+=(--project-name tilesfst --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}")

export TILESFST_DEPLOY_ENV_FILE="${ENV_FILE}"
docker compose "${DOCKER_COMPOSE_ARGS[@]}" run --rm "${SERVICE}" \
  uv run --no-sync python -m app.modules.media.maintenance "${TASK}" "$@"
