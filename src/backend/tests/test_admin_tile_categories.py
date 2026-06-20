"""Admin tile categories API integration tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_category(
    client: TestClient,
    headers: dict[str, str],
    *,
    name: str,
    code: str,
    parent_id: int | None = None,
    sort_order: int = 10,
) -> int:
    payload: dict = {"name": name, "code": code, "sort_order": sort_order}
    if parent_id is not None:
        payload["parent_id"] = parent_id
    response = client.post("/api/v1/admin/tile-categories", headers=headers, json=payload)
    assert response.status_code == 200, response.text
    return response.json()["data"]["id"]


def test_list_categories_and_tree(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    list_resp = client.get("/api/v1/admin/tile-categories", headers=headers)
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert body["code"] == 0
    assert "summary" in body["data"]

    tree_resp = client.get("/api/v1/admin/tile-categories/tree", headers=headers)
    assert tree_resp.status_code == 200
    assert isinstance(tree_resp.json()["data"], list)


def test_create_category_hierarchy(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    root_id = _create_category(client, headers, name="按材质", code="CAT-MAT")
    child_id = _create_category(
        client, headers, name="大理石瓷砖", code="CAT-MARBLE", parent_id=root_id
    )

    detail = client.get(f"/api/v1/admin/tile-categories/{child_id}", headers=headers)
    assert detail.status_code == 200
    data = detail.json()["data"]
    assert data["level"] == 2
    assert "按材质" in data["path"]


def test_max_depth_exceeded(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    l1 = _create_category(client, headers, name="L1", code="CAT-L1-DEPTH")
    l2 = _create_category(client, headers, name="L2", code="CAT-L2-DEPTH", parent_id=l1)
    l3 = _create_category(client, headers, name="L3", code="CAT-L3-DEPTH", parent_id=l2)

    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "L4", "code": "CAT-L4-DEPTH", "sort_order": 10, "parent_id": l3},
    )
    assert response.status_code == 422
    assert response.json()["code"] == 30023


def test_duplicate_code(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    payload = {"name": "Dup A", "code": "CAT-DUP-TEST", "sort_order": 10}
    assert client.post("/api/v1/admin/tile-categories", headers=headers, json=payload).status_code == 200
    response = client.post("/api/v1/admin/tile-categories", headers=headers, json=payload)
    assert response.status_code == 409
    assert response.json()["code"] == 30021


def test_delete_forbidden_when_enabled(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cat_id = _create_category(client, headers, name="Enabled Cat", code="CAT-EN-DEL")
    response = client.delete(f"/api/v1/admin/tile-categories/{cat_id}", headers=headers)
    assert response.status_code == 409
    assert response.json()["code"] == 30022


def test_delete_success_when_disabled(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cat_id = _create_category(client, headers, name="Delete Cat", code="CAT-DEL-OK")
    client.post(f"/api/v1/admin/tile-categories/{cat_id}/disable", headers=headers)
    response = client.delete(f"/api/v1/admin/tile-categories/{cat_id}", headers=headers)
    assert response.status_code == 200


def test_filter_by_parent_id(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    root_id = _create_category(client, headers, name="Filter Root", code="CAT-FILTER-ROOT")
    _create_category(
        client, headers, name="Filter Child", code="CAT-FILTER-CHILD", parent_id=root_id
    )

    response = client.get(
        "/api/v1/admin/tile-categories",
        headers=headers,
        params={"parent_id": root_id},
    )
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    ids = {item["id"] for item in items}
    assert root_id in ids


def test_employee_can_access_categories(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if not repo.get_by_username("operator01"):
            repo.create_user(
                username="operator01",
                password="Operator123!",
                display_name="运营一号",
                role="employee",
            )
    finally:
        session.close()

    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/tile-categories", headers=headers)
    assert response.status_code == 200
