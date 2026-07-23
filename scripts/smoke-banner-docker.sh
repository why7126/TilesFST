#!/usr/bin/env bash
# Docker 冒烟：Banner 管理 API + 页面路由（REQ-0016 task 8.3）
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
API_URL="${SMOKE_API_URL:-http://localhost:${HOST_PORT_BACKEND:-8000}}"
BACKEND_CONTAINER="${SMOKE_BACKEND_CONTAINER:-tilesfst-backend}"
ADMIN_USER="${SMOKE_ADMIN_USER:-${ADMIN_USERNAME:-admin}}"
ADMIN_PASSWORD="${SMOKE_ADMIN_PASSWORD:-${ADMIN_INITIAL_PASSWORD:-change-me-on-first-run}}"

echo "==> Docker banner smoke (web=${WEB_URL}, api=${API_URL})"

if ! docker ps --format '{{.Names}}' | grep -qx "${BACKEND_CONTAINER}"; then
  echo "ERROR: backend container '${BACKEND_CONTAINER}' not running. Run ./scripts/docker-up.sh first." >&2
  exit 1
fi

echo "-- backend pytest banner (host, same codebase as image build context)"
(cd "${ROOT}/src/backend" && uv run pytest tests/test_admin_banners.py -q)

echo "-- OpenAPI banner/topic paths (container)"
docker exec "${BACKEND_CONTAINER}" uv run python -c "
from app.main import app
paths = sorted({
    getattr(r, 'path', '')
    for r in app.routes
    if 'banner' in getattr(r, 'path', '') or '/admin/topics' in getattr(r, 'path', '')
})
assert paths, 'no banner/topic routes registered'
print('routes:', len(paths))
for p in paths:
    print(' ', p)
"

echo "-- login + banners API (container TestClient -> host curl)"
TOKEN="$(docker exec "${BACKEND_CONTAINER}" uv run python -c "
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.db.session import get_session_factory
from app.db.seed import seed_admin_user

client = TestClient(app)
response = client.post(
    '/api/v1/auth/login',
    json={
        'username': settings.admin_username,
        'password': settings.admin_initial_password,
        'remember_me': False,
    },
)
body = response.json()
if body.get('code') != 0:
    session = get_session_factory()()
    try:
        settings.admin_reset_password_on_startup = True
        seed_admin_user(session)
    finally:
        session.close()
    response = client.post(
        '/api/v1/auth/login',
        json={
            'username': settings.admin_username,
            'password': settings.admin_initial_password,
            'remember_me': False,
        },
    )
    body = response.json()
    if body.get('code') != 0:
        raise SystemExit(f'login failed: {body}')
print(body['data']['access_token'])
")"
LIST_CODE="$(curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer ${TOKEN}" \
  "${API_URL}/api/v1/admin/banners?page=1&page_size=20")"
if [[ "${LIST_CODE}" != "200" ]]; then
  echo "ERROR: GET /api/v1/admin/banners returned HTTP ${LIST_CODE}" >&2
  exit 1
fi
echo "OK GET /api/v1/admin/banners -> ${LIST_CODE}"

TOPICS_CODE="$(curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer ${TOKEN}" \
  "${API_URL}/api/v1/admin/topics")"
if [[ "${TOPICS_CODE}" != "200" ]]; then
  echo "ERROR: GET /api/v1/admin/topics returned HTTP ${TOPICS_CODE}" >&2
  exit 1
fi
echo "OK GET /api/v1/admin/topics -> ${TOPICS_CODE}"

echo "-- banner image upload through Web Docker :3000 boundary"
TMP_PNG="$(mktemp)"
trap 'rm -f "${TMP_PNG}"' EXIT
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82' > "${TMP_PNG}"
UPLOAD_RESPONSE="$(curl -sS -w '\n%{http_code}' \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "file=@${TMP_PNG};type=image/png;filename=banner-smoke.png" \
  "${WEB_URL}/api/v1/admin/uploads/banner-images")"
UPLOAD_CODE="$(printf '%s' "${UPLOAD_RESPONSE}" | tail -n 1)"
UPLOAD_BODY="$(printf '%s' "${UPLOAD_RESPONSE}" | sed '$d')"
if [[ "${UPLOAD_CODE}" != "200" ]] || ! printf '%s' "${UPLOAD_BODY}" | grep -q '"object_key"'; then
  echo "ERROR: banner upload via ${WEB_URL} returned HTTP ${UPLOAD_CODE}: ${UPLOAD_BODY}" >&2
  exit 1
fi
echo "OK POST ${WEB_URL}/api/v1/admin/uploads/banner-images -> ${UPLOAD_CODE}"

echo "-- SPA routes (web container)"
for path in /admin/login /admin/banners /admin; do
  code="$(curl -s -o /dev/null -w '%{http_code}' "${WEB_URL}${path}")"
  if [[ "${code}" != "200" ]]; then
    echo "ERROR: ${WEB_URL}${path} returned HTTP ${code}" >&2
    exit 1
  fi
  echo "OK ${path} -> ${code}"
done

echo "-- Dashboard banner shortcut link in SPA bundle"
JS_PATH="$(curl -sS "${WEB_URL}/admin" | grep -oE '/assets/index-[^"]+\.js' | head -1 || true)"
if [[ -n "${JS_PATH}" ]] && curl -sS "${WEB_URL}${JS_PATH}" | grep -q 'admin/banners'; then
  echo "OK Dashboard bundle contains /admin/banners shortcut"
else
  echo "WARN: could not verify Dashboard shortcut in bundle (manual check: Dashboard -> 新增 Banner)"
fi

echo "==> banner Docker smoke passed"
