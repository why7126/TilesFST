#!/usr/bin/env bash
# Docker 冒烟：瓷砖规格 API + 页面路由（REQ-0009 task 8.3）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "${ROOT}/.env" ]]; then
  # shellcheck disable=SC1091
  set -a
  # shellcheck source=/dev/null
  source "${ROOT}/.env"
  set +a
fi

WEB_URL="${SMOKE_WEB_URL:-http://localhost:${HOST_PORT_WEB:-3000}}"
BACKEND_CONTAINER="${SMOKE_BACKEND_CONTAINER:-tilesfst-backend}"

echo "==> Docker tile-spec smoke (web=${WEB_URL})"

if ! docker ps --format '{{.Names}}' | grep -qx "${BACKEND_CONTAINER}"; then
  echo "ERROR: backend container '${BACKEND_CONTAINER}' not running. Run ./scripts/docker-up.sh first." >&2
  exit 1
fi

echo "-- backend pytest (host, against same codebase as container image)"
(cd "${ROOT}/src/backend" && uv run pytest tests/test_tile_specs.py tests/test_admin_tile_skus.py -q)

echo "-- OpenAPI tile-specs paths (container)"
docker exec "${BACKEND_CONTAINER}" uv run python -c "
from app.main import app
paths = sorted({getattr(r, 'path', '') for r in app.routes if 'tile-spec' in getattr(r, 'path', '')})
assert paths, 'no tile-spec routes registered'
print('routes:', len(paths))
for p in paths:
    print(' ', p)
"

echo "-- SPA routes (web container)"
for path in /admin/login /admin/tile-specs /admin/tile-skus; do
  code="$(curl -s -o /dev/null -w '%{http_code}' "${WEB_URL}${path}")"
  if [[ "${code}" != "200" ]]; then
    echo "ERROR: ${WEB_URL}${path} returned HTTP ${code}" >&2
    exit 1
  fi
  echo "OK ${path} -> ${code}"
done

echo "==> tile-spec Docker smoke passed"
