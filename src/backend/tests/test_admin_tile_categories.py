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
    parent_id: int | None = None,
    sort_order: int = 10,
) -> int:
    payload: dict = {"name": name, "sort_order": sort_order}
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
    assert body["data"]["summary"]["max_level"] == 2

    tree_resp = client.get("/api/v1/admin/tile-categories/tree", headers=headers)
    assert tree_resp.status_code == 200
    assert isinstance(tree_resp.json()["data"], list)


def test_create_category_hierarchy(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    root_id = _create_category(client, headers, name="按材质")
    child_id = _create_category(client, headers, name="大理石", parent_id=root_id)

    detail = client.get(f"/api/v1/admin/tile-categories/{child_id}", headers=headers)
    assert detail.status_code == 200
    data = detail.json()["data"]
    assert data["level"] == 2
    assert "按材质" in data["path"]
    assert data["code"].startswith("CAT-")


def test_max_depth_exceeded(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    l1 = _create_category(client, headers, name="L1")
    l2 = _create_category(client, headers, name="L2", parent_id=l1)

    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "L3", "sort_order": 10, "parent_id": l2},
    )
    assert response.status_code == 422
    assert response.json()["code"] == 30023
    assert "二级" in response.json()["message"]


def test_level_filter_rejects_third_level(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get(
        "/api/v1/admin/tile-categories",
        headers=headers,
        params={"level": 3},
    )
    assert response.status_code == 422
    assert response.json()["code"] == 30023


def test_create_category_generates_code_and_ignores_client_code(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "自动编码", "code": "CLIENT-CODE", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["code"].startswith("CAT-")
    assert data["code"] != "CLIENT-CODE"


def test_category_name_validation(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cases = [
        ("", "类目名称不能为空"),
        ("一二三四五六七八九十A", "类目名称不能超过 10 个字符"),
        ("含 空格", "类目名称只能包含中文、英文和数字"),
        ("bad-name", "类目名称只能包含中文、英文和数字"),
    ]

    for name, message in cases:
        response = client.post(
            "/api/v1/admin/tile-categories",
            headers=headers,
            json={"name": name, "sort_order": 10},
        )
        assert response.status_code in {400, 422}
        assert message in response.json()["message"]


def test_duplicate_name_same_parent_and_update_self_exclusion(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    root_a = _create_category(client, headers, name="同名父A")
    root_b = _create_category(client, headers, name="同名父B")
    child_a = _create_category(client, headers, name="同名", parent_id=root_a)
    _create_category(client, headers, name="同名", parent_id=root_b)

    duplicate = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "同名", "sort_order": 20, "parent_id": root_a},
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == 30024

    self_update = client.put(
        f"/api/v1/admin/tile-categories/{child_a}",
        headers=headers,
        json={"name": "同名", "sort_order": 15, "description": "仅更新排序"},
    )
    assert self_update.status_code == 200, self_update.text

    other = _create_category(client, headers, name="另一名", parent_id=root_a)
    dup_update = client.put(
        f"/api/v1/admin/tile-categories/{other}",
        headers=headers,
        json={"name": "同名", "sort_order": 10},
    )
    assert dup_update.status_code == 409
    assert dup_update.json()["code"] == 30024


def test_delete_forbidden_when_enabled(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cat_id = _create_category(client, headers, name="启用删除")
    response = client.delete(f"/api/v1/admin/tile-categories/{cat_id}", headers=headers)
    assert response.status_code == 409
    assert response.json()["code"] == 30022


def test_delete_success_when_disabled(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cat_id = _create_category(client, headers, name="停用删除")
    client.post(f"/api/v1/admin/tile-categories/{cat_id}/disable", headers=headers)
    response = client.delete(f"/api/v1/admin/tile-categories/{cat_id}", headers=headers)
    assert response.status_code == 200


def test_filter_by_parent_id(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    root_id = _create_category(client, headers, name="筛选父级")
    _create_category(client, headers, name="筛选子级", parent_id=root_id)

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
