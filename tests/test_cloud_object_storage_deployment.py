from __future__ import annotations

from pathlib import Path

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

    assert 'ENV NGINX_ENVSUBST_FILTER="^UPLOAD_"' in dockerfile
    assert 'ENV UPLOAD_CLIENT_MAX_BODY_SIZE="512m"' in dockerfile
    assert 'ENV UPLOAD_PROXY_READ_TIMEOUT_SECONDS="600"' in dockerfile
    assert 'ENV UPLOAD_PROXY_REQUEST_BUFFERING="off"' in dockerfile
    assert "COPY src/web/nginx.conf.template /etc/nginx/templates/default.conf.template" in dockerfile
    assert "location /api/v1/admin/uploads/" in template
    assert template.index("location /api/v1/admin/uploads/") < template.index("location /api/ {")
    assert "client_max_body_size ${UPLOAD_CLIENT_MAX_BODY_SIZE};" in template
    assert "client_body_timeout ${UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS}s;" in template
    assert "proxy_connect_timeout ${UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS}s;" in template
    assert "proxy_send_timeout ${UPLOAD_PROXY_SEND_TIMEOUT_SECONDS}s;" in template
    assert "proxy_read_timeout ${UPLOAD_PROXY_READ_TIMEOUT_SECONDS}s;" in template
    assert "send_timeout ${UPLOAD_SEND_TIMEOUT_SECONDS}s;" in template
    assert "proxy_request_buffering ${UPLOAD_PROXY_REQUEST_BUFFERING};" in template
    assert "proxy_set_header Host $host;" in template


def test_all_compose_variants_pass_upload_nginx_defaults_to_web_service() -> None:
    for compose_file in [
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "docker-compose.prod.external.yml",
    ]:
        compose = _compose(compose_file)
        web_environment = compose["services"]["web"]["environment"]

        assert web_environment == UPLOAD_NGINX_ENV_DEFAULTS
