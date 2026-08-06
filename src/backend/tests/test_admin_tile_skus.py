"""Admin tile SKU API integration tests."""

from __future__ import annotations

from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import text

from app.db.seed import DEFAULT_ADMIN_USERNAME
from app.db.session import get_session_factory
from app.modules.media.storage import (
    StoredMediaObject,
    get_media_storage_client,
    same_directory_thumbnail_object_key,
)
from app.repositories.task_trace_repository import TaskTraceRepository
from app.repositories.tile_sku_repository import TileSkuRepository
from app.repositories.user_repository import UserRepository
from app.services.task_trace_service import TaskTraceService
from tests.test_auth import _login, client  # noqa: F401 — re-export fixture


def _image_bytes(fmt: str = "JPEG", size: tuple[int, int] = (960, 640)) -> bytes:
    image = Image.new("RGB", size, (120, 30, 200))
    output = BytesIO()
    image.save(output, format=fmt, quality=95)
    return output.getvalue()


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


def _create_category(
    client: TestClient, headers: dict[str, str], *, parent_id: int | None = None
) -> int:
    suffix = uuid4().hex[:6]
    payload = {"name": f"测类{suffix[:4]}", "sort_order": 10}
    if parent_id is not None:
        payload["parent_id"] = parent_id
    response = client.post(
        "/api/v1/admin/tile-categories",
        headers=headers,
        json=payload,
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
    name: str = "Test SKU",
) -> dict:
    payload = {
        "save_mode": save_mode,
        "name": name,
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


def _set_sku_times(
    sku_id: int,
    *,
    status: str,
    published_at: str | None,
    created_at: str,
    updated_at: str,
) -> None:
    session = get_session_factory()()
    try:
        session.execute(
            text(
                """
                UPDATE tiles
                SET status = :status,
                    published_at = :published_at,
                    created_at = :created_at,
                    updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": sku_id,
                "status": status,
                "published_at": published_at,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )
        session.commit()
    finally:
        session.close()


def _main_image_key(sku_id: int) -> str:
    session = get_session_factory()()
    try:
        row = (
            session.execute(
                text(
                    """
                    SELECT object_key FROM tile_images
                    WHERE tile_id = :id AND is_main = 1
                    ORDER BY sort_order, id
                    LIMIT 1
                    """
                ),
                {"id": sku_id},
            )
            .mappings()
            .one()
        )
        return str(row["object_key"])
    finally:
        session.close()


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


def test_create_sku_records_task_trace_spans_and_request_log(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    )

    assert response.status_code == 200
    data = response.json()["data"]
    task_trace_id = data["task_trace_id"]
    assert task_trace_id.startswith("task_sku_create_")
    assert data["task_type"] == "sku_create"

    session = get_session_factory()()
    try:
        trace = (
            session.execute(
                text(
                    """
                    SELECT task_type, status, resource_type, resource_id, error_code
                    FROM task_traces
                    WHERE task_trace_id = :task_trace_id
                    """
                ),
                {"task_trace_id": task_trace_id},
            )
            .mappings()
            .one()
        )
        spans = (
            session.execute(
                text(
                    """
                    SELECT span_name, status, request_id, resource_id
                    FROM task_trace_spans
                    WHERE task_trace_id = :task_trace_id
                    ORDER BY sequence ASC
                    """
                ),
                {"task_trace_id": task_trace_id},
            )
            .mappings()
            .all()
        )
        request_log = (
            session.execute(
                text(
                    """
                    SELECT request_id, task_type
                    FROM request_logs
                    WHERE task_trace_id = :task_trace_id
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                ),
                {"task_trace_id": task_trace_id},
            )
            .mappings()
            .one()
        )
    finally:
        session.close()

    assert trace["task_type"] == "sku_create"
    assert trace["status"] == "success"
    assert trace["resource_type"] == "tile_sku"
    assert trace["resource_id"] == str(data["id"])
    assert trace["error_code"] is None
    assert [span["span_name"] for span in spans] == [
        "api_receive",
        "input_validate",
        "business_persist",
        "api_response",
    ]
    assert {span["status"] for span in spans} == {"success"}
    assert {span["request_id"] for span in spans} == {response.headers["x-request-id"]}
    assert spans[-1]["resource_id"] == str(data["id"])
    assert request_log["request_id"] == response.headers["x-request-id"]
    assert request_log["task_type"] == "sku_create"


def test_update_sku_business_error_records_failed_task_trace(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    )
    sku_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/api/v1/admin/tile-skus/{sku_id}",
        headers=headers,
        json={
            "name": "Invalid Brand SKU",
            "brand_id": 999999,
            "category_id": category_id,
            "spec_id": spec_id,
            "reference_price": 10,
        },
    )

    assert response.status_code == 400
    assert response.json()["code"] == 40001
    session = get_session_factory()()
    try:
        trace = (
            session.execute(
                text(
                    """
                    SELECT task_trace_id, status, error_code
                    FROM task_traces
                    WHERE task_type = 'sku_update'
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                )
            )
            .mappings()
            .one()
        )
        failed_span = (
            session.execute(
                text(
                    """
                    SELECT span_name, status, error_code
                    FROM task_trace_spans
                    WHERE task_trace_id = :task_trace_id AND status = 'failed'
                    ORDER BY sequence DESC
                    LIMIT 1
                    """
                ),
                {"task_trace_id": trace["task_trace_id"]},
            )
            .mappings()
            .one()
        )
    finally:
        session.close()

    assert trace["status"] == "failed"
    assert trace["error_code"] == "40001"
    assert failed_span["span_name"] == "business_process"
    assert failed_span["error_code"] == "40001"


def test_task_trace_context_helpers_for_async_and_safe_failure(monkeypatch) -> None:
    session = get_session_factory()()
    try:
        service = TaskTraceService(TaskTraceRepository(session))
        context = service.build_context(
            task_type="sku_create",
            task_trace_id="invalid id",
            request_id="req_001",
            actor_user_id="user_001",
            resource_type="tile_sku",
            resource_id="42",
        )
        assert context.task_trace_id.startswith("task_sku_create_")
        assert TaskTraceService.serialize_async_context(context) == {
            "task_trace_id": context.task_trace_id,
            "task_type": "sku_create",
            "parent_request_id": "req_001",
            "actor_user_id": "user_001",
            "client_type": "web_admin",
            "resource_type": "tile_sku",
            "resource_id": "42",
        }

        def fail_record_context_span(*_args, **_kwargs) -> None:
            raise RuntimeError("trace table unavailable")

        monkeypatch.setattr(service, "record_context_span", fail_record_context_span)
        assert service.record_context_span_safe(context, span_name="api_receive") is False
    finally:
        session.close()


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


def test_upload_tile_video_then_save_sku_video_closure(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)

    upload = client.post(
        "/api/v1/admin/uploads/tile-videos",
        headers=headers,
        files={"file": ("closure.mp4", b"\x00\x00\x00 ftypmp42closure", "video/mp4")},
    )
    assert upload.status_code == 200
    upload_data = upload.json()["data"]
    object_key = upload_data["object_key"]
    assert upload_data["url"] == f"/media/{object_key}"

    payload = _create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id)
    payload["videos"] = [
        {
            "object_key": object_key,
            "file_name": "closure.mp4",
            "file_size_bytes": 21,
            "duration_seconds": None,
            "sort_order": 0,
        }
    ]

    create_response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)
    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["video_count"] == 1

    detail = client.get(f"/api/v1/admin/tile-skus/{created['id']}", headers=headers)
    assert detail.status_code == 200
    videos = detail.json()["data"]["videos"]
    assert videos[0]["object_key"] == object_key
    assert videos[0]["url"] == f"/media/{object_key}"
    assert videos[0]["file_name"] == "closure.mp4"


def test_create_sku_formalizes_pending_tile_image(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)

    upload = client.post(
        "/api/v1/admin/uploads/tile-images",
        headers=headers,
        files={"file": ("pending-main.jpg", _image_bytes("JPEG", (960, 640)), "image/jpeg")},
    )
    assert upload.status_code == 200
    pending_key = upload.json()["data"]["object_key"]
    assert pending_key.startswith("images/default/tiles/pending/")

    payload = _create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id)
    payload["images"] = [
        {
            "object_key": pending_key,
            "url": f"/media/{pending_key}",
            "is_main": True,
            "sort_order": 0,
        }
    ]
    create_response = client.post("/api/v1/admin/tile-skus", headers=headers, json=payload)

    assert create_response.status_code == 200
    created = create_response.json()["data"]
    image = created["images"][0]
    assert image["object_key"].startswith(f"images/default/tiles/{created['id']}/")
    assert "/pending/" not in image["object_key"]
    assert image["url"] == f"/media/{image['object_key']}"

    storage = get_media_storage_client()
    thumbnail_key = same_directory_thumbnail_object_key(image["object_key"])
    assert pending_key in storage.objects
    assert image["object_key"] in storage.objects
    assert thumbnail_key in storage.objects
    assert storage.objects[thumbnail_key].content != storage.objects[image["object_key"]].content
    assert len(storage.objects[thumbnail_key].content) < len(storage.objects[image["object_key"]].content)
    media = client.get(image["url"])
    assert media.status_code == 200
    assert media.content == storage.objects[image["object_key"]].content

    publish = client.post(f"/api/v1/admin/tile-skus/{created['id']}/publish", headers=headers)
    assert publish.status_code == 200
    public_list = client.get("/api/v1/miniapp/products", params={"page": 1, "pageSize": 50})
    assert public_list.status_code == 200
    public_item = next(
        item
        for item in public_list.json()["data"]["items"]
        if item["product_id"] == created["id"]
    )
    assert "/pending/" not in public_item["cover_image"]
    assert public_item["cover_image"].startswith("/media/images/default/tiles/")


def test_update_sku_formalizes_new_pending_tile_image(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    created = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    ).json()["data"]

    upload = client.post(
        "/api/v1/admin/uploads/tile-images",
        headers=headers,
        files={"file": ("new-main.webp", _image_bytes("WEBP", (960, 640)), "image/webp")},
    )
    assert upload.status_code == 200
    pending_key = upload.json()["data"]["object_key"]

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
                    "object_key": pending_key,
                    "url": f"/media/{pending_key}",
                    "is_main": True,
                    "sort_order": 0,
                }
            ],
        },
    )

    assert update.status_code == 200
    image = update.json()["data"]["images"][0]
    assert image["object_key"].startswith(f"images/default/tiles/{created['id']}/")
    assert "/pending/" not in image["object_key"]
    assert image["object_key"] == _main_image_key(created["id"])
    assert same_directory_thumbnail_object_key(image["object_key"]) in get_media_storage_client().objects


def test_publish_sku_blocks_when_pending_image_formalization_fails(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    created = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    ).json()["data"]

    pending_key = f"images/default/tiles/pending/{uuid4().hex}.jpg"
    storage = get_media_storage_client()
    storage.objects[pending_key] = StoredMediaObject(b"\xff\xd8\xffpending", "image/jpeg")
    session = get_session_factory()()
    try:
        session.execute(
            text(
                """
                UPDATE tile_images
                SET object_key = :object_key, url = :url
                WHERE tile_id = :tile_id AND is_main = 1
                """
            ),
            {
                "tile_id": created["id"],
                "object_key": pending_key,
                "url": f"/media/{pending_key}",
            },
        )
        session.commit()
    finally:
        session.close()

    storage.fail_put = True
    publish = client.post(f"/api/v1/admin/tile-skus/{created['id']}/publish", headers=headers)

    assert publish.status_code == 409
    assert _main_image_key(created["id"]) == pending_key
    detail = client.get(f"/api/v1/admin/tile-skus/{created['id']}", headers=headers)
    assert detail.json()["data"]["status"] == "DRAFT"


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


def test_admin_list_tile_skus_includes_main_image_thumbnail_url(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(
            brand_id=brand_id,
            category_id=category_id,
            spec_id=spec_id,
            sku_code=f"SKU-THUMB-{uuid4().hex[:6]}",
        ),
    )
    assert response.status_code == 200

    list_response = client.get("/api/v1/admin/tile-skus", headers=headers)
    assert list_response.status_code == 200
    item = next(
        item for item in list_response.json()["data"]["items"] if item["id"] == response.json()["data"]["id"]
    )
    assert item["main_image_url"] == "/media/tiles/1/images/main.jpg"
    assert item["main_image_thumbnail_url"] == "/media/tiles/1/images/main.thumb.jpg"


def test_admin_list_tile_skus_includes_published_at(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)

    draft_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    )
    assert draft_response.status_code == 200
    draft = draft_response.json()["data"]

    draft_list = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": draft["sku_code"], "status": "DRAFT"},
    )
    assert draft_list.status_code == 200
    draft_body = draft_list.json()["data"]
    assert draft_body["pagination"]["total"] == 1
    assert draft_body["items"][0]["published_at"] is None
    assert "summary" in draft_body

    publish_response = client.post(
        f"/api/v1/admin/tile-skus/{draft['id']}/publish",
        headers=headers,
    )
    assert publish_response.status_code == 200

    published_list = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": draft["sku_code"], "status": "PUBLISHED"},
    )
    assert published_list.status_code == 200
    published_body = published_list.json()["data"]
    item = published_body["items"][0]
    assert published_body["pagination"]["total"] == 1
    assert isinstance(item["published_at"], str)
    assert published_body["summary"]["total"] >= 1


def test_admin_list_tile_skus_uses_publish_state_business_time_order(
    client: TestClient,
) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    prefix = f"排序回归 {uuid4().hex[:8]}"

    def create_named_sku(label: str, *, save_mode: str = "create") -> int:
        response = client.post(
            "/api/v1/admin/tile-skus",
            headers=headers,
            json=_create_sku_payload(
                brand_id=brand_id,
                category_id=category_id,
                spec_id=spec_id,
                save_mode=save_mode,
                name=f"{prefix} {label}",
            ),
        )
        assert response.status_code == 200
        return int(response.json()["data"]["id"])

    published_old_id = create_named_sku("已发布旧时间")
    published_new_id = create_named_sku("已发布新时间")
    published_null_id = create_named_sku("已发布空时间")
    draft_old_id = create_named_sku("草稿旧创建", save_mode="draft")
    disabled_same_time_id = create_named_sku("下架同创建")
    draft_new_id = create_named_sku("草稿新创建", save_mode="draft")
    published_page_ids = [
        create_named_sku(f"已发布分页旧 {index}")
        for index in range(1, 6)
    ]

    _set_sku_times(
        published_old_id,
        status="PUBLISHED",
        published_at="2026-07-01T09:00:00+00:00",
        created_at="2026-06-01T09:00:00+00:00",
        updated_at="2026-07-10T09:00:00+00:00",
    )
    _set_sku_times(
        published_new_id,
        status="PUBLISHED",
        published_at="2026-07-03T09:00:00+00:00",
        created_at="2026-06-02T09:00:00+00:00",
        updated_at="2026-07-02T09:00:00+00:00",
    )
    _set_sku_times(
        published_null_id,
        status="PUBLISHED",
        published_at=None,
        created_at="2026-06-03T09:00:00+00:00",
        updated_at="2026-07-12T09:00:00+00:00",
    )
    _set_sku_times(
        draft_old_id,
        status="DRAFT",
        published_at=None,
        created_at="2026-07-02T09:00:00+00:00",
        updated_at="2026-07-20T09:00:00+00:00",
    )
    _set_sku_times(
        disabled_same_time_id,
        status="DISABLED",
        published_at="2026-07-04T09:00:00+00:00",
        created_at="2026-07-02T09:00:00+00:00",
        updated_at="2026-07-21T09:00:00+00:00",
    )
    _set_sku_times(
        draft_new_id,
        status="DRAFT",
        published_at=None,
        created_at="2026-07-04T09:00:00+00:00",
        updated_at="2026-07-01T09:00:00+00:00",
    )
    for index, sku_id in enumerate(published_page_ids, start=1):
        _set_sku_times(
            sku_id,
            status="PUBLISHED",
            published_at=f"2026-06-{10 - index:02d}T09:00:00+00:00",
            created_at=f"2026-05-{10 - index:02d}T09:00:00+00:00",
            updated_at=f"2026-07-{10 - index:02d}T09:00:00+00:00",
        )

    response = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": prefix, "page_size": 20},
    )

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert [item["name"].removeprefix(f"{prefix} ") for item in items] == [
        "草稿新创建",
        "下架同创建",
        "草稿旧创建",
        "已发布新时间",
        "已发布旧时间",
        "已发布分页旧 1",
        "已发布分页旧 2",
        "已发布分页旧 3",
        "已发布分页旧 4",
        "已发布分页旧 5",
        "已发布空时间",
    ]
    assert items[0]["published_at"] is None
    assert items[1]["published_at"] == "2026-07-04T09:00:00+00:00"
    assert items[3]["published_at"] == "2026-07-03T09:00:00+00:00"
    assert items[10]["published_at"] is None

    page_response = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": prefix, "page": 2, "page_size": 10},
    )

    assert page_response.status_code == 200
    page_items = page_response.json()["data"]["items"]
    assert [item["name"].removeprefix(f"{prefix} ") for item in page_items] == [
        "已发布空时间",
    ]

    draft_response = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": prefix, "status": "DRAFT", "page_size": 10},
    )

    assert draft_response.status_code == 200
    draft_items = draft_response.json()["data"]["items"]
    assert [item["name"].removeprefix(f"{prefix} ") for item in draft_items] == [
        "草稿新创建",
        "草稿旧创建",
    ]


def test_publish_sku_refreshes_published_at_when_restored(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)
    create_response = client.post(
        "/api/v1/admin/tile-skus",
        headers=headers,
        json=_create_sku_payload(brand_id=brand_id, category_id=category_id, spec_id=spec_id),
    )
    assert create_response.status_code == 200
    sku_id = create_response.json()["data"]["id"]

    first_publish = client.post(f"/api/v1/admin/tile-skus/{sku_id}/publish", headers=headers)
    assert first_publish.status_code == 200
    assert first_publish.json()["data"]["published_at"]

    unpublish = client.post(f"/api/v1/admin/tile-skus/{sku_id}/unpublish", headers=headers)
    assert unpublish.status_code == 200
    first_published_at = first_publish.json()["data"]["published_at"]
    assert unpublish.json()["data"]["published_at"] == first_published_at

    disabled_list = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": create_response.json()["data"]["sku_code"], "status": "DISABLED"},
    )
    assert disabled_list.status_code == 200
    assert disabled_list.json()["data"]["items"][0]["published_at"] == first_published_at

    stale_published_at = "2000-01-01T00:00:00+00:00"
    session = get_session_factory()()
    try:
        session.execute(
            text("UPDATE tiles SET published_at = :published_at WHERE id = :id"),
            {"published_at": stale_published_at, "id": sku_id},
        )
        session.commit()
    finally:
        session.close()

    restored = client.post(f"/api/v1/admin/tile-skus/{sku_id}/publish", headers=headers)
    assert restored.status_code == 200
    restored_published_at = restored.json()["data"]["published_at"]
    assert isinstance(restored_published_at, str)
    assert restored_published_at != stale_published_at

    listed = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"keyword": create_response.json()["data"]["sku_code"], "status": "PUBLISHED"},
    )
    assert listed.status_code == 200
    assert listed.json()["data"]["items"][0]["published_at"] == restored_published_at


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


def test_list_filter_by_parent_category_includes_child_skus(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    brand_id = _create_brand(client, headers)
    parent_category_id = _create_category(client, headers)
    child_category_id = _create_category(client, headers, parent_id=parent_category_id)
    sibling_category_id = _create_category(client, headers)
    spec_id = _create_spec(client, headers)

    for category_id, name in [
        (parent_category_id, "父类目筛选命中 SKU"),
        (child_category_id, "子类目筛选命中 SKU"),
        (sibling_category_id, "同级类目不命中 SKU"),
    ]:
        response = client.post(
            "/api/v1/admin/tile-skus",
            headers=headers,
            json=_create_sku_payload(
                brand_id=brand_id,
                category_id=category_id,
                spec_id=spec_id,
                name=name,
            ),
        )
        assert response.status_code == 200

    response = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={"category_id": parent_category_id},
    )

    assert response.status_code == 200
    names = {item["name"] for item in response.json()["data"]["items"]}
    assert "父类目筛选命中 SKU" in names
    assert "子类目筛选命中 SKU" in names
    assert "同级类目不命中 SKU" not in names


def test_list_filter_by_child_category_combines_with_other_filters(client: TestClient) -> None:
    headers = _auth_headers(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    matching_brand_id = _create_brand(client, headers)
    other_brand_id = _create_brand(client, headers)
    parent_category_id = _create_category(client, headers)
    child_category_id = _create_category(client, headers, parent_id=parent_category_id)
    spec_id = _create_spec(client, headers)

    cases = [
        (matching_brand_id, child_category_id, "柔光组合命中 SKU"),
        (other_brand_id, child_category_id, "柔光组合其他品牌 SKU"),
        (matching_brand_id, parent_category_id, "柔光组合父类目 SKU"),
        (matching_brand_id, child_category_id, "其他名称 SKU"),
    ]
    for brand_id, category_id, name in cases:
        response = client.post(
            "/api/v1/admin/tile-skus",
            headers=headers,
            json=_create_sku_payload(
                brand_id=brand_id,
                category_id=category_id,
                spec_id=spec_id,
                name=name,
            ),
        )
        assert response.status_code == 200

    response = client.get(
        "/api/v1/admin/tile-skus",
        headers=headers,
        params={
            "category_id": child_category_id,
            "brand_id": matching_brand_id,
            "keyword": "柔光",
            "material_completeness": "missing_videos",
        },
    )

    assert response.status_code == 200
    names = {item["name"] for item in response.json()["data"]["items"]}
    assert "柔光组合命中 SKU" in names
    assert "柔光组合其他品牌 SKU" not in names
    assert "柔光组合父类目 SKU" not in names
    assert "其他名称 SKU" not in names
