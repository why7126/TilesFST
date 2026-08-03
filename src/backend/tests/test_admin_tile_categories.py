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


def test_category_tree_returns_direct_children_count(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    root_id = _create_category(client, headers, name="子类目计数")
    first_child = _create_category(client, headers, name="子类目一", parent_id=root_id)
    second_child = _create_category(client, headers, name="子类目二", parent_id=root_id)

    response = client.get("/api/v1/admin/tile-categories/tree", headers=headers)
    assert response.status_code == 200, response.text

    tree = response.json()["data"]
    root = next(node for node in tree if node["id"] == root_id)
    assert root["children_count"] == 2
    assert root["sku_count"] == 0

    children = {node["id"]: node for node in root["children"]}
    assert children[first_child]["children_count"] == 0
    assert children[second_child]["children_count"] == 0


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


def test_create_category_accepts_fifteen_character_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "一二三四五六七八九十12345", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["name"] == "一二三四五六七八九十12345"


def test_update_category_accepts_fifteen_character_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    category_id = _create_category(client, headers, name="边界更新")
    response = client.put(
        f"/api/v1/admin/tile-categories/{category_id}",
        headers=headers,
        json={"name": "更新一二三四五六七八九十123", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["name"] == "更新一二三四五六七八九十123"


def test_create_category_accepts_special_character_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "岩板-大规格/客厅", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["name"] == "岩板-大规格/客厅"
    assert response.json()["data"]["path"] == "岩板-大规格/客厅"


def test_update_category_accepts_special_character_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    category_id = _create_category(client, headers, name="特殊更新")
    response = client.put(
        f"/api/v1/admin/tile-categories/{category_id}",
        headers=headers,
        json={"name": "600x1200(亮面)", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["name"] == "600x1200(亮面)"


def test_create_category_accepts_chinese_parentheses_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": "墙砖（哑光）", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["name"] == "墙砖（哑光）"
    assert data["path"] == "墙砖（哑光）"


def test_update_category_accepts_chinese_parentheses_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    category_id = _create_category(client, headers, name="中文括号更新")
    response = client.put(
        f"/api/v1/admin/tile-categories/{category_id}",
        headers=headers,
        json={"name": "地砖（防滑）", "sort_order": 10},
    )
    assert response.status_code == 200, response.text
    assert response.json()["data"]["name"] == "地砖（防滑）"

    detail = client.get(f"/api/v1/admin/tile-categories/{category_id}", headers=headers)
    assert detail.status_code == 200, detail.text
    assert detail.json()["data"]["name"] == "地砖（防滑）"


def test_update_category_rejects_sixteen_character_name(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    category_id = _create_category(client, headers, name="边界拒绝")
    response = client.put(
        f"/api/v1/admin/tile-categories/{category_id}",
        headers=headers,
        json={"name": "一二三四五六七八九十123456", "sort_order": 10},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 40001
    assert "类目名称最多 15 个字符" in response.json()["message"]


def test_category_name_validation(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    cases = [
        ("", "类目名称不能为空"),
        ("一二三四五六七八九十123456", "类目名称最多 15 个字符"),
        ("含 空格", "类目名称仅支持中文、英文、数字和特殊字符"),
        ("含\n换行", "类目名称仅支持中文、英文、数字和特殊字符"),
        ("含\t制表", "类目名称仅支持中文、英文、数字和特殊字符"),
        ("bad<name", "类目名称仅支持中文、英文、数字和特殊字符"),
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
