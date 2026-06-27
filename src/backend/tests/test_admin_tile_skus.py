"""Admin tile SKU API integration tests."""

from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.user_repository import UserRepository
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _auth_headers(client: TestClient, username: str, password: str) -> dict[str, str]:
    data = _login(client, username, password)
    return {"Authorization": f"Bearer {data['access_token']}"}


def _create_employee() -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        if repo.get_by_username("operator01"):
            return
        repo.create_user(
            username="operator01",
            password="Operator123!",
            display_name="运营一号",
            role="employee",
        )
    finally:
        session.close()


def _create_brand(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={"name": f"SKU Test Brand {suffix}", "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_category(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:6]
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json={"name": f"SKU Test Category {suffix}", "code": f"SKU-CAT-{suffix}", "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_sku_payload(
    *,
    brand_id: int,
    category_id: int,
    sku_code: str = "SKU-TEST-001",
    save_mode: str = "create",
) -> dict:
    return {
        "save_mode": save_mode,
        "name": "Test SKU",
        "sku_code": sku_code,
        "brand_id": brand_id,
        "category_id": category_id,
        "size": "900×1800mm",
        "surface_finish": "亮光面",
        "reference_price": 268.0,
        "images": [
            {
                "object_key": "tiles/1/images/main.jpg",
                "url": "/media/tiles/1/images/main.jpg",
                "is_main": True,
                "sort_order": 0,
            }
        ],
    }


def test_create_sku_without_surface_finish(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-NO-FINISH-001"
    )
    payload.pop("surface_finish")
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["surface_finish"] == "-"


def test_create_sku_requires_reference_price(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-NO-PRICE-001"
    )
    payload["reference_price"] = None
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 422


def test_create_sku_with_zero_reference_price(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-ZERO-PRICE-001"
    )
    payload["reference_price"] = 0.0
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["reference_price"] == 0.0


def test_publish_sku_with_empty_surface_finish(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-PUB-NO-FINISH-001"
    )
    payload.pop("surface_finish")
    create_response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    sku_id = create_response.json()["data"]["id"]

    publish = client.post(f"/api/v1/admin/tile-skus/{sku_id}/publish", headers=headers)
    assert publish.status_code == 200
    assert publish.json()["data"]["status"] == "PUBLISHED"


def test_admin_list_tile_skus(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get("/api/v1/admin/tile-skus", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert "items" in body["data"]
    assert "summary" in body["data"]


def test_employee_can_access_tile_skus_api(client: TestClient) -> None:
    _create_employee()
    headers = _auth_headers(client, "operator01", "Operator123!")
    response = client.get("/api/v1/admin/tile-skus", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_create_sku_draft_and_create(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)

    draft_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json={"save_mode": "draft", "name": "Draft Only SKU"},
    )
    assert draft_response.status_code == 200
    draft = draft_response.json()["data"]
    assert draft["status"] == "DRAFT"
    assert draft["name"] == "Draft Only SKU"

    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id),
    )
    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["sku_code"] == "SKU-TEST-001"
    assert created["status"] == "DRAFT"
    assert created["has_main_image"] is True


def test_create_sku_needs_completion_without_main_image(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-NO-MAIN-001"
    )
    payload.pop("images")
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "NEEDS_COMPLETION"


def test_duplicate_sku_code(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-DUPE-001"
    )
    assert client.post("/api/v1/admin/tile-skus", headers=headers, json=payload).status_code == 200
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 409
    assert response.json()["code"] == 30031


def test_publish_and_unpublish_sku(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, sku_code="SKU-PUB-001"
        ),
    )
    sku_id = create_response.json()["data"]["id"]

    publish = client.post(f"/api/v1/admin/tile-skus/{sku_id}/publish", headers=headers)
    assert publish.status_code == 200
    assert publish.json()["data"]["status"] == "PUBLISHED"

    unpublish = client.post(f"/api/v1/admin/tile-skus/{sku_id}/unpublish", headers=headers)
    assert unpublish.status_code == 200
    assert unpublish.json()["data"]["status"] == "DISABLED"


def test_publish_forbidden_without_main_image(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, sku_code="SKU-PUB-FAIL-001"
    )
    payload.pop("images")
    create_response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    sku_id = create_response.json()["data"]["id"]

    response = client.post(f"/api/v1/admin/tile-skus/{sku_id}/publish", headers=headers)
    assert response.status_code == 409
    assert response.json()["code"] == 30033


def test_delete_published_forbidden(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, sku_code="SKU-DEL-FAIL-001"
        ),
    )
    sku_id = create_response.json()["data"]["id"]
    client.post(f"/api/v1/admin/tile-skus/{sku_id}/publish", headers=headers)

    response = client.delete(f"/api/v1/admin/tile-skus/{sku_id}", headers=headers)
    assert response.status_code == 409
    assert response.json()["code"] == 30032


def test_delete_draft_sku(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, sku_code="SKU-DEL-OK-001"
        ),
    )
    sku_id = create_response.json()["data"]["id"]
    response = client.delete(f"/api/v1/admin/tile-skus/{sku_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_list_filter_by_material_completeness(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, sku_code="SKU-FILTER-001"
        ),
    )
    response = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"material_completeness": "missing_videos"},
    )
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert all(item["material_completeness"] == "missing_videos" for item in items)
