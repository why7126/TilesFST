from __future__ import annotations

from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]


UPLOAD_NGINX_ENV_DEFAULTS = {
    "NGINX_ENVSUBST_FILTER": "^UPLOAD_",
    "UPLOAD_CLIENT_MAX_BODY_SIZE": "${UPLOAD_CLIENT_MAX_BODY_SIZE:-512m}",
    "UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS": "${UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS:-600}",
    "UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS": "${UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS:-60}",
    "UPLOAD_PROXY_SEND_TIMEOUT_SECONDS": "${UPLOAD_PROXY_SEND_TIMEOUT_SECONDS:-600}",
    "UPLOAD_PROXY_READ_TIMEOUT_SECONDS": "${UPLOAD_PROXY_READ_TIMEOUT_SECONDS:-600}",
    "UPLOAD_SEND_TIMEOUT_SECONDS": "${UPLOAD_SEND_TIMEOUT_SECONDS:-600}",
    "UPLOAD_PROXY_REQUEST_BUFFERING": "${UPLOAD_PROXY_REQUEST_BUFFERING:-off}",
}


def _compose(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text())


def _nginx_location_block(config: str, location: str) -> str:
    match = re.search(rf"location {re.escape(location)} \{{(?P<body>.*?)\n    \}}", config, re.S)
    assert match, f"missing nginx location {location}"
    return match.group("body")


def test_external_prod_compose_only_runs_app_services_and_passes_object_storage_env() -> None:
    compose = _compose("docker-compose.prod.external.yml")
    services = compose["services"]

    assert sorted(services) == ["backend", "web"]
    assert "minio" not in services
    assert "minio-init" not in services
    assert "mysql" not in services

    environment = services["backend"]["environment"]
    assert environment["OBJECT_STORAGE_PROVIDER"] == "${OBJECT_STORAGE_PROVIDER:-s3-compatible}"
    assert environment["OBJECT_STORAGE_ENDPOINT"] == "${OBJECT_STORAGE_ENDPOINT:?Set external object storage endpoint, for example cos.example.com}"
    assert environment["OBJECT_STORAGE_ACCESS_KEY"] == "${OBJECT_STORAGE_ACCESS_KEY:?Set external object storage access key}"
    assert environment["OBJECT_STORAGE_SECRET_KEY"] == "${OBJECT_STORAGE_SECRET_KEY:?Set external object storage secret key}"
    assert environment["OBJECT_STORAGE_BUCKET"] == "${OBJECT_STORAGE_BUCKET:?Set existing external object storage bucket}"
    assert environment["OBJECT_STORAGE_AUTO_CREATE_BUCKET"] == "${OBJECT_STORAGE_AUTO_CREATE_BUCKET:-false}"
    assert "MINIO_ENDPOINT" not in environment
    assert "MINIO_ACCESS_KEY" not in environment
    assert "MINIO_SECRET_KEY" not in environment
    assert "MINIO_BUCKET" not in environment


def test_self_hosted_prod_compose_keeps_minio_and_enables_auto_create_bucket() -> None:
    compose = _compose("docker-compose.prod.yml")
    services = compose["services"]

    assert {"backend", "web", "minio", "minio-init"}.issubset(services)
    environment = services["backend"]["environment"]
    assert environment["OBJECT_STORAGE_PROVIDER"] == "self-hosted-minio"
    assert environment["OBJECT_STORAGE_ENDPOINT"] == "minio:9000"
    assert environment["OBJECT_STORAGE_PATH_STYLE"] == "true"
    assert environment["OBJECT_STORAGE_AUTO_CREATE_BUCKET"] == "true"
    assert "MINIO_ENDPOINT" not in environment
    assert "MINIO_ACCESS_KEY" not in environment
    assert "MINIO_SECRET_KEY" not in environment
    assert "MINIO_BUCKET" not in environment


def test_default_local_compose_does_not_start_minio_without_profile() -> None:
    compose = _compose("docker-compose.yml")
    services = compose["services"]

    assert sorted(name for name, service in services.items() if "profiles" not in service) == [
        "backend",
        "web",
    ]
    assert services["minio"]["profiles"] == ["self-hosted-storage"]
    assert services["minio-init"]["profiles"] == ["self-hosted-storage"]


def test_web_nginx_uses_runtime_template_for_upload_timeout_env() -> None:
    dockerfile = (ROOT / "src/web/Dockerfile").read_text()
    template = (ROOT / "src/web/nginx.conf.template").read_text()
    exact_upload_block = _nginx_location_block(template, "= /api/v1/admin/uploads")
    upload_prefix_block = _nginx_location_block(template, "/api/v1/admin/uploads/")

    assert 'ENV NGINX_ENVSUBST_FILTER="^UPLOAD_"' in dockerfile
    assert 'ENV UPLOAD_CLIENT_MAX_BODY_SIZE="512m"' in dockerfile
    assert 'ENV UPLOAD_PROXY_READ_TIMEOUT_SECONDS="600"' in dockerfile
    assert 'ENV UPLOAD_PROXY_REQUEST_BUFFERING="off"' in dockerfile
    assert "COPY src/web/nginx.conf.template /etc/nginx/templates/default.conf.template" in dockerfile
    assert "location = /api/v1/admin/uploads" in template
    assert "location /api/v1/admin/uploads/" in template
    assert template.index("location = /api/v1/admin/uploads") < template.index("location /api/v1/admin/uploads/")
    assert template.index("location /api/v1/admin/uploads/") < template.index("location /api/ {")
    assert "proxy_pass http://tilesfst-backend:8000/api/v1/admin/uploads;" in exact_upload_block
    assert "return 301" not in exact_upload_block
    assert "rewrite " not in exact_upload_block
    assert "proxy_pass http://tilesfst-backend:8000/api/v1/admin/uploads/;" in upload_prefix_block
    for block in [exact_upload_block, upload_prefix_block]:
        assert "client_max_body_size ${UPLOAD_CLIENT_MAX_BODY_SIZE};" in block
        assert "client_body_timeout ${UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS}s;" in block
        assert "proxy_connect_timeout ${UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS}s;" in block
        assert "proxy_send_timeout ${UPLOAD_PROXY_SEND_TIMEOUT_SECONDS}s;" in block
        assert "proxy_read_timeout ${UPLOAD_PROXY_READ_TIMEOUT_SECONDS}s;" in block
        assert "send_timeout ${UPLOAD_SEND_TIMEOUT_SECONDS}s;" in block
        assert "proxy_request_buffering ${UPLOAD_PROXY_REQUEST_BUFFERING};" in block
        assert "proxy_set_header Host $host;" in block


def test_static_web_nginx_matches_upload_template_routes() -> None:
    config = (ROOT / "src/web/nginx.conf").read_text()
    exact_upload_block = _nginx_location_block(config, "= /api/v1/admin/uploads")
    upload_prefix_block = _nginx_location_block(config, "/api/v1/admin/uploads/")

    assert config.index("location = /api/v1/admin/uploads") < config.index("location /api/v1/admin/uploads/")
    assert config.index("location /api/v1/admin/uploads/") < config.index("location /api/ {")
    assert "proxy_pass http://tilesfst-backend:8000/api/v1/admin/uploads;" in exact_upload_block
    assert "return 301" not in exact_upload_block
    assert "rewrite " not in exact_upload_block
    assert "proxy_pass http://tilesfst-backend:8000/api/v1/admin/uploads/;" in upload_prefix_block
    for block in [exact_upload_block, upload_prefix_block]:
        assert "client_max_body_size 512m;" in block
        assert "client_body_timeout 600s;" in block
        assert "proxy_connect_timeout 60s;" in block
        assert "proxy_send_timeout 600s;" in block
        assert "proxy_read_timeout 600s;" in block
        assert "send_timeout 600s;" in block
        assert "proxy_request_buffering off;" in block
        assert "proxy_set_header Host $host;" in block


def test_all_compose_variants_pass_upload_nginx_defaults_to_web_service() -> None:
    for compose_file in [
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "docker-compose.prod.external.yml",
    ]:
        compose = _compose(compose_file)
        web_environment = compose["services"]["web"]["environment"]

        assert web_environment == UPLOAD_NGINX_ENV_DEFAULTS
