"""Admin tile SKU API integration tests."""

from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.repositories.tile_sku_repository import TileSkuRepository
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
        json={"name": f"测类{suffix[:4]}", "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_spec(client: TestClient, headers: dict[str, str]) -> int:
    suffix = uuid4().hex[:4]
    width = 600 + int(suffix[:2], 16) % 200
    length = 1200 + int(suffix[2:], 16) % 200
    response = client.post(
        "/api/v1/admin/tile-specs",
        headers=headers,
        json={"width_mm": width, "length_mm": length, "sort_order": 10},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def _create_sku_payload(
    *,
    brand_id: int,
    category_id: int,
    spec_id: int,
    sku_code: str | None = None,
    save_mode: str = "create",
) -> dict:
    payload = {
        "save_mode": save_mode,
        "name": "Test SKU",
        "brand_id": brand_id,
        "category_id": category_id,
        "spec_id": spec_id,
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
    if sku_code is not None:
        payload["sku_code"] = sku_code
    return payload


def test_create_sku_without_surface_finish(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-NO-FINISH-001"
    )
    payload.pop("surface_finish")
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["surface_finish"] == "-"


def test_create_sku_requires_reference_price(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-NO-PRICE-001"
    )
    payload["reference_price"] = None
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 422


def test_create_sku_with_zero_reference_price(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-ZERO-PRICE-001"
    )
    payload["reference_price"] = 0.0
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["reference_price"] == 0.0


def test_publish_sku_with_empty_surface_finish(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-PUB-NO-FINISH-001"
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
    spec_id = _create_spec(client, headers)

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
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    )
    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["sku_code"].startswith("SKU-")
    assert created["status"] == "DRAFT"
    assert created["has_main_image"] is True


def test_create_sku_ignores_manual_sku_code(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id,
        category_id=category_id,
        spec_id=spec_id,
        sku_code="SKU-MANUAL-IGNORED",
    )

    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["sku_code"].startswith("SKU-")
    assert data["sku_code"] != "SKU-MANUAL-IGNORED"


def test_create_sku_needs_completion_without_main_image(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-NO-MAIN-001"
    )
    payload.pop("images")
    response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "NEEDS_COMPLETION"


def test_generated_sku_code_collision_retries(client: TestClient, monkeypatch) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    generated = iter(["SKU-DUPE-001", "SKU-DUPE-001", "SKU-DUPE-RETRY-OK"])
    monkeypatch.setattr(
        TileSkuRepository,
        "generate_sku_code",
        staticmethod(lambda: next(generated)),
    )
    payload = _create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id)
    assert client.post("/api/v1/admin/tile-skus", headers=headers, json=payload).status_code == 200

    response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id,
            category_id=category_id,
            spec_id=spec_id,
        ),
    )

    assert response.status_code == 200
    assert response.json()["data"]["sku_code"] == "SKU-DUPE-RETRY-OK"


def test_update_sku_keeps_generated_code_stable(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id,
            category_id=category_id,
            spec_id=spec_id,
        ),
    )
    created = create_response.json()["data"]

    update = client.put(
        f"/api/v1/admin/tile-skus/{created['id']}",
        headers=headers,
        json={
            "name": "Updated Product Name",
            "sku_code": "SKU-SHOULD-NOT-CHANGE",
            "brand_id": brand_id,
            "category_id": category_id,
            "spec_id": spec_id,
            "reference_price": created["reference_price"],
        },
    )

    assert update.status_code == 200
    data = update.json()["data"]
    assert data["name"] == "Updated Product Name"
    assert data["sku_code"] == created["sku_code"]


def test_update_sku_images_removes_missing_images_and_moves_main_first(
    client: TestClient,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id,
            category_id=category_id,
            spec_id=spec_id,
        ),
    )
    created = create_response.json()["data"]

    update = client.put(
        f"/api/v1/admin/tile-skus/{created['id']}",
        headers=headers,
        json={
            "name": created["name"],
            "brand_id": brand_id,
            "category_id": category_id,
            "spec_id": spec_id,
            "reference_price": created["reference_price"],
            "images": [
                {
                    "object_key": "tiles/1/images/removed.jpg",
                    "url": "/media/tiles/1/images/removed.jpg",
                    "is_main": False,
                    "sort_order": 0,
                },
                {
                    "object_key": "tiles/1/images/secondary.jpg",
                    "url": "/media/tiles/1/images/secondary.jpg",
                    "is_main": False,
                    "sort_order": 1,
                },
                {
                    "object_key": "tiles/1/images/new-main.jpg",
                    "url": "/media/tiles/1/images/new-main.jpg",
                    "is_main": True,
                    "sort_order": 2,
                },
            ],
        },
    )

    assert update.status_code == 200
    images = update.json()["data"]["images"]
    assert [img["object_key"] for img in images] == [
        "tiles/1/images/new-main.jpg",
        "tiles/1/images/removed.jpg",
        "tiles/1/images/secondary.jpg",
    ]
    assert [img["is_main"] for img in images] == [True, False, False]
    assert [img["sort_order"] for img in images] == [0, 1, 2]

    update_without_removed = client.put(
        f"/api/v1/admin/tile-skus/{created['id']}",
        headers=headers,
        json={
            "name": created["name"],
            "brand_id": brand_id,
            "category_id": category_id,
            "spec_id": spec_id,
            "reference_price": created["reference_price"],
            "images": [
                {
                    "object_key": "tiles/1/images/new-main.jpg",
                    "url": "/media/tiles/1/images/new-main.jpg",
                    "is_main": True,
                    "sort_order": 0,
                },
                {
                    "object_key": "tiles/1/images/secondary.jpg",
                    "url": "/media/tiles/1/images/secondary.jpg",
                    "is_main": False,
                    "sort_order": 1,
                },
            ],
        },
    )

    assert update_without_removed.status_code == 200
    images = update_without_removed.json()["data"]["images"]
    assert [img["object_key"] for img in images] == [
        "tiles/1/images/new-main.jpg",
        "tiles/1/images/secondary.jpg",
    ]


def test_update_sku_images_accepts_empty_list(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id,
            category_id=category_id,
            spec_id=spec_id,
        ),
    )
    created = create_response.json()["data"]

    update = client.put(
        f"/api/v1/admin/tile-skus/{created['id']}",
        headers=headers,
        json={
            "name": created["name"],
            "brand_id": brand_id,
            "category_id": category_id,
            "spec_id": spec_id,
            "reference_price": created["reference_price"],
            "images": [],
        },
    )

    assert update.status_code == 200
    data = update.json()["data"]
    assert data["images"] == []
    assert data["has_main_image"] is False
    assert data["material_completeness"] == "missing_images"


def test_publish_and_unpublish_sku(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-PUB-001"
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
    spec_id = _create_spec(client, headers)
    payload = _create_sku_payload(
        brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-PUB-FAIL-001"
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
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-DEL-FAIL-001"
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
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-DEL-OK-001"
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
    spec_id = _create_spec(client, headers)
    client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id, category_id=category_id, spec_id=spec_id, sku_code="SKU-FILTER-001"
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
