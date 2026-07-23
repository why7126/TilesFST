from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_external_prod_compose_only_runs_app_services_and_passes_object_storage_env() -> None:
    compose = yaml.safe_load((ROOT / "docker-compose.prod.external.yml").read_text())
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
    compose = yaml.safe_load((ROOT / "docker-compose.prod.yml").read_text())
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
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
    services = compose["services"]

    assert sorted(name for name, service in services.items() if "profiles" not in service) == [
        "backend",
        "web",
    ]
    assert services["minio"]["profiles"] == ["self-hosted-storage"]
    assert services["minio-init"]["profiles"] == ["self-hosted-storage"]
