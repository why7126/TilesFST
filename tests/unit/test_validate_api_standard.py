from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load_validator() -> ModuleType:
    script_path = ROOT / "scripts" / "validate-api-standard.py"
    spec = importlib.util.spec_from_file_location("validate_api_standard", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_openapi(path: Path, tags: list[str]) -> None:
    path.write_text(
        json.dumps(
            {
                "openapi": "3.1.0",
                "paths": {
                    "/api/v1/example": {
                        "get": {
                            "operationId": "getExample",
                            "tags": tags,
                            "responses": {"200": {"description": "OK"}},
                        }
                    }
                },
            }
        ),
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    ("tags", "expected"),
    [
        (["auth", "profile"], "必须且只能有 1 个"),
        (["auth", "auth"], "存在重复值"),
        (["Admin Users"], "非 kebab-case"),
    ],
)
def test_openapi_operation_tag_drift_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tags: list[str], expected: str
) -> None:
    validator = _load_validator()
    openapi_path = tmp_path / "openapi.json"
    _write_openapi(openapi_path, tags)

    monkeypatch.setattr(validator, "OPENAPI_PATH", openapi_path)
    validator.violations.clear()

    validator.check_openapi_operation_tags()

    assert any(expected in violation for violation in validator.violations)
    assert any("GET /api/v1/example (getExample)" in violation for violation in validator.violations)


def test_openapi_operation_single_kebab_case_tag_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    validator = _load_validator()
    openapi_path = tmp_path / "openapi.json"
    _write_openapi(openapi_path, ["admin-users"])

    monkeypatch.setattr(validator, "OPENAPI_PATH", openapi_path)
    validator.violations.clear()

    validator.check_openapi_operation_tags()

    assert validator.violations == []
