#!/usr/bin/env bash
# Docker 冒烟：系统设置 API + 页面路由（add-system-settings task 10.2）
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
BACKEND_CONTAINER="${SMOKE_BACKEND_CONTAINER:-tile-info-platform-backend}"

echo "==> Docker system-settings smoke (web=${WEB_URL}, api=${API_URL})"

if ! docker ps --format '{{.Names}}' | grep -qx "${BACKEND_CONTAINER}"; then
  echo "ERROR: backend container '${BACKEND_CONTAINER}' not running. Run ./scripts/docker-up.sh first." >&2
  exit 1
fi

echo "-- backend pytest system_settings (host)"
(cd "${ROOT}/src/backend" && uv run pytest tests/test_system_settings.py -q)

echo "-- OpenAPI system-settings paths (container)"
docker exec "${BACKEND_CONTAINER}" uv run python -c "
from app.main import app
paths = sorted({
    getattr(r, 'path', '')
    for r in app.routes
    if 'system-settings' in getattr(r, 'path', '')
})
assert paths, 'no system-settings routes registered'
print('routes:', len(paths))
for p in paths:
    print(' ', p)
"

echo "-- login + system-settings API (container TestClient -> host curl)"
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

BASIC_CODE="$(curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer ${TOKEN}" \
  "${API_URL}/api/v1/admin/system-settings/basic")"
if [[ "${BASIC_CODE}" != "200" ]]; then
  echo "ERROR: GET /api/v1/admin/system-settings/basic returned HTTP ${BASIC_CODE}" >&2
  exit 1
fi
echo "OK GET /api/v1/admin/system-settings/basic -> ${BASIC_CODE}"

echo "-- employee 403 on system-settings"
EMP_TOKEN="$(docker exec "${BACKEND_CONTAINER}" uv run python -c "
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository

session = get_session_factory()()
repo = UserRepository(session)
if not repo.get_by_username('operator01'):
    repo.create_user(username='operator01', password='Operator123!', display_name='运营', role='employee')
session.close()

client = TestClient(app)
resp = client.post('/api/v1/auth/login', json={'username': 'operator01', 'password': 'Operator123!', 'remember_me': False})
print(resp.json()['data']['access_token'])
")"
EMP_CODE="$(curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer ${EMP_TOKEN}" \
  "${API_URL}/api/v1/admin/system-settings/basic")"
if [[ "${EMP_CODE}" != "403" ]]; then
  echo "ERROR: employee GET system-settings expected 403, got ${EMP_CODE}" >&2
  exit 1
fi
echo "OK employee GET system-settings -> ${EMP_CODE}"

echo "-- SPA routes (web container)"
for path in /admin/login /admin/settings/basic /admin; do
  code="$(curl -s -o /dev/null -w '%{http_code}' "${WEB_URL}${path}")"
  if [[ "${code}" != "200" ]]; then
    echo "ERROR: ${WEB_URL}${path} returned HTTP ${code}" >&2
    exit 1
  fi
  echo "OK ${path} -> ${code}"
done

echo "==> system-settings Docker smoke passed"
