"""Validation envelope integration tests."""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient


def _admin_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "AdminPass123!",
            "remember_me": False,
        },
    )
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _assert_validation_envelope(payload: dict[str, Any]) -> list[dict[str, Any]]:
    assert set(payload) == {"code", "message", "data"}
    assert payload["code"] == 40001
    assert payload["message"] == "请求参数无效"
    assert "detail" not in payload
    errors = payload["data"]["errors"]
    assert isinstance(errors, list)
    assert errors
    for item in errors:
        assert set(item) == {"field", "message", "type", "location"}
        assert isinstance(item["field"], str)
        assert isinstance(item["message"], str)
        assert isinstance(item["type"], str)
        assert isinstance(item["location"], list)
    return errors


def test_admin_json_body_validation_uses_unified_envelope(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)

    response = api_client.post(
        "/api/v1/admin/users",
        headers=headers,
        json={"username": "validuser", "display_name": "Valid User"},
    )

    assert response.status_code == 422
    errors = _assert_validation_envelope(response.json())
    assert any(item["field"] == "role" for item in errors)


def test_admin_query_validation_uses_unified_envelope(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)

    response = api_client.get("/api/v1/admin/users?page=0", headers=headers)

    assert response.status_code == 422
    errors = _assert_validation_envelope(response.json())
    assert any(item["field"] == "query.page" for item in errors)


def test_admin_upload_missing_file_validation_uses_unified_envelope(
    api_client: TestClient,
) -> None:
    headers = _admin_headers(api_client)

    response = api_client.post("/api/v1/admin/uploads/brand-logos", headers=headers)

    assert response.status_code == 422
    text = response.text
    assert "AdminPass123!" not in text
    assert "Authorization" not in text
    assert "MINIO" not in text
    assert "/Users/" not in text
    errors = _assert_validation_envelope(response.json())
    assert any(item["field"] == "file" for item in errors)


def test_business_app_error_is_not_overwritten_by_validation_handler(
    api_client: TestClient,
) -> None:
    headers = _admin_headers(api_client)
    payload = {"username": "validuser", "display_name": "Valid User", "role": "employee"}

    first = api_client.post("/api/v1/admin/users", headers=headers, json=payload)
    assert first.status_code == 200

    second = api_client.post("/api/v1/admin/users", headers=headers, json=payload)

    assert second.status_code == 409
    assert second.json() == {"code": 40910, "message": "用户名已存在", "data": None}


def test_representative_admin_openapi_uses_validation_envelope_schema(
    api_client: TestClient,
) -> None:
    response = api_client.get("/openapi.json")
    assert response.status_code == 200

    openapi = response.json()
    create_user_422 = openapi["paths"]["/api/v1/admin/users"]["post"]["responses"]["422"]
    upload_422 = openapi["paths"]["/api/v1/admin/uploads/brand-logos"]["post"]["responses"]["422"]

    assert create_user_422["content"]["application/json"]["schema"]["$ref"].endswith(
        "/ApiValidationErrorResponse"
    )
    assert upload_422["content"]["application/json"]["schema"]["$ref"].endswith(
        "/ApiValidationErrorResponse"
    )
