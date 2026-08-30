"""Admin brand certificate integration tests."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.modules.media.storage import (
    StoredMediaObject,
    same_directory_thumbnail_object_key,
    set_media_storage_client,
)


@dataclass
class InMemoryMediaStorage:
    objects: dict[str, StoredMediaObject]

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        self.objects[object_key] = StoredMediaObject(content=content, content_type=content_type)

    def get_object(self, object_key: str) -> StoredMediaObject:
        return self.objects[object_key]


def _admin_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "AdminPass123!", "remember_me": False},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['data']['access_token']}"}


def _image_bytes(fmt: str = "WEBP", size: tuple[int, int] = (900, 600)) -> bytes:
    image = Image.new("RGB", size, (90, 120, 180))
    output = BytesIO()
    image.save(output, format=fmt)
    return output.getvalue()


def _create_brand(client: TestClient, headers: dict[str, str], name: str = "蒙娜丽莎") -> int:
    response = client.post(
        "/api/v1/admin/brands",
        headers=headers,
        json={"name": name, "sort_order": 10},
    )
    assert response.status_code == 200
    return int(response.json()["data"]["id"])


def _employee_headers(client: TestClient, admin_headers: dict[str, str]) -> dict[str, str]:
    create = client.post(
        "/api/v1/admin/users",
        headers=admin_headers,
        json={
            "username": "certemployee",
            "display_name": "证书员工",
            "role": "employee",
        },
    )
    assert create.status_code == 200
    password = create.json()["data"]["initial_password"]
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "certemployee", "password": password, "remember_me": False},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['data']['access_token']}"}


def _file_payload(name: str = "iso.pdf") -> dict:
    return {
        "file_url": "/media/files/default/brand-certificates/test.pdf",
        "file_key": "files/default/brand-certificates/test.pdf",
        "file_name": name,
        "file_mime_type": "application/pdf",
        "file_size_bytes": 128,
    }


def _image_payload(
    *,
    name: str,
    key: str,
    is_main: bool,
    sort_order: int,
) -> dict:
    return {
        "file_url": f"/media/{key}",
        "file_key": key,
        "file_name": name,
        "file_mime_type": "image/webp",
        "file_size_bytes": 256,
        "is_main": is_main,
        "sort_order": sort_order,
    }


def _certificate_payload(brand_id: int, name: str = "ISO 9001 质量管理体系认证") -> dict:
    return {
        "brand_id": brand_id,
        "name": name,
        "sort_order": 10,
        "type": "QUALITY",
        "certificate_no": "ISO-001",
        "issuer": "认证机构",
        "file": _file_payload(),
        "is_permanent": False,
        "effective_date": "2026-01-01",
        "expiry_date": "2026-12-31",
        "is_visible": True,
        "remark": "年度证书",
    }


def test_brand_certificate_crud_filter_visibility_and_delete(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)
    brand_id = _create_brand(api_client, headers)

    create = api_client.post(
        "/api/v1/admin/brand-certificates",
        headers=headers,
        json=_certificate_payload(brand_id),
    )
    assert create.status_code == 200
    cert = create.json()["data"]
    assert cert["brand_id"] == brand_id
    assert cert["validity_status"] in {"VALID", "EXPIRING_SOON", "EXPIRED"}
    assert cert["display_status"] == "VISIBLE"

    duplicate = api_client.post(
        "/api/v1/admin/brand-certificates",
        headers=headers,
        json=_certificate_payload(brand_id),
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == 30014

    listed = api_client.get(
        "/api/v1/admin/brand-certificates",
        headers=headers,
        params={"keyword": "ISO", "brand_id": brand_id, "type": "QUALITY"},
    )
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1
    assert listed.json()["data"]["summary"]["total"] == 1

    hidden = api_client.post(
        f"/api/v1/admin/brand-certificates/{cert['id']}/hide",
        headers=headers,
    )
    assert hidden.status_code == 200
    assert hidden.json()["data"]["display_status"] == "HIDDEN"

    shown = api_client.post(
        f"/api/v1/admin/brand-certificates/{cert['id']}/show",
        headers=headers,
    )
    assert shown.status_code == 200
    assert shown.json()["data"]["display_status"] == "VISIBLE"

    blocked_delete_brand = api_client.delete(f"/api/v1/admin/brands/{brand_id}", headers=headers)
    assert blocked_delete_brand.status_code == 409
    assert "证书" in blocked_delete_brand.json()["message"]

    deleted = api_client.delete(f"/api/v1/admin/brand-certificates/{cert['id']}", headers=headers)
    assert deleted.status_code == 200

    after_delete = api_client.get("/api/v1/admin/brand-certificates", headers=headers)
    assert after_delete.status_code == 200
    assert after_delete.json()["data"]["total"] == 0


def test_brand_certificate_validation_errors(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)
    brand_id = _create_brand(api_client, headers, "东鹏")
    payload = _certificate_payload(brand_id)
    payload["expiry_date"] = "2025-01-01"

    response = api_client.post("/api/v1/admin/brand-certificates", headers=headers, json=payload)

    assert response.status_code == 400
    assert response.json()["code"] == 40024


def test_brand_certificate_saves_images_main_order_and_image_only_fallback(
    api_client: TestClient,
) -> None:
    headers = _admin_headers(api_client)
    brand_id = _create_brand(api_client, headers, "多图品牌")
    payload = _certificate_payload(brand_id, "多页检测报告")
    payload["file"] = None
    payload["images"] = [
        _image_payload(
            name="page-2.webp",
            key="images/default/brand-certificates/page-2.webp",
            is_main=False,
            sort_order=20,
        ),
        _image_payload(
            name="cover.webp",
            key="images/default/brand-certificates/cover.webp",
            is_main=True,
            sort_order=10,
        ),
    ]

    create = api_client.post("/api/v1/admin/brand-certificates", headers=headers, json=payload)

    assert create.status_code == 200
    data = create.json()["data"]
    assert data["file_key"] == "images/default/brand-certificates/cover.webp"
    assert data["thumbnail_url"] == "/media/images/default/brand-certificates/cover.thumb.webp"
    assert data["main_image"]["file_name"] == "cover.webp"
    assert data["main_image"]["thumbnail_url"] == "/media/images/default/brand-certificates/cover.thumb.webp"
    assert [image["file_name"] for image in data["images"]] == ["cover.webp", "page-2.webp"]
    assert [image["thumbnail_url"] for image in data["images"]] == [
        "/media/images/default/brand-certificates/cover.thumb.webp",
        "/media/images/default/brand-certificates/page-2.thumb.webp",
    ]
    assert [image["sort_order"] for image in data["images"]] == [0, 1]
    assert [image["is_main"] for image in data["images"]] == [True, False]

    detail = api_client.get(f"/api/v1/admin/brand-certificates/{data['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["main_image"]["file_key"].endswith("cover.webp")

    listed = api_client.get("/api/v1/admin/brand-certificates", headers=headers)
    assert listed.status_code == 200
    listed_item = listed.json()["data"]["items"][0]
    assert listed_item["main_image"]["file_name"] == "cover.webp"
    assert len(listed_item["images"]) == 2


def test_brand_certificate_rejects_invalid_main_image_payload(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)
    brand_id = _create_brand(api_client, headers, "主图校验品牌")
    payload = _certificate_payload(brand_id, "多主图检测报告")
    payload["images"] = [
        _image_payload(
            name="a.webp",
            key="files/default/brand-certificates/a.webp",
            is_main=True,
            sort_order=0,
        ),
        _image_payload(
            name="b.webp",
            key="files/default/brand-certificates/b.webp",
            is_main=True,
            sort_order=1,
        ),
    ]

    response = api_client.post("/api/v1/admin/brand-certificates", headers=headers, json=payload)

    assert response.status_code == 400
    assert response.json()["code"] == 40026


def test_brand_certificate_rejects_forged_image_reference(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)
    brand_id = _create_brand(api_client, headers, "伪造引用品牌")
    payload = _certificate_payload(brand_id, "伪造图片检测报告")
    payload["images"] = [
        {
            **_image_payload(
                name="evil.webp",
                key="https://example.com/evil.webp",
                is_main=True,
                sort_order=0,
            ),
            "file_url": "https://example.com/evil.webp",
        }
    ]

    response = api_client.post("/api/v1/admin/brand-certificates", headers=headers, json=payload)

    assert response.status_code == 400
    assert response.json()["code"] == 40027


def test_employee_can_list_but_cannot_mutate_brand_certificates(api_client: TestClient) -> None:
    admin_headers = _admin_headers(api_client)
    employee_headers = _employee_headers(api_client, admin_headers)
    brand_id = _create_brand(api_client, admin_headers, "权限品牌")

    listed = api_client.get("/api/v1/admin/brand-certificates", headers=employee_headers)
    assert listed.status_code == 200

    created = api_client.post(
        "/api/v1/admin/brand-certificates",
        headers=employee_headers,
        json=_certificate_payload(brand_id),
    )
    assert created.status_code == 403
    assert created.json()["code"] == 40302


def test_brand_certificate_upload_accepts_pdf_and_rejects_invalid_type(
    api_client: TestClient,
) -> None:
    storage = InMemoryMediaStorage(objects={})
    set_media_storage_client(storage)
    headers = _admin_headers(api_client)
    try:
        pdf = api_client.post(
            "/api/v1/admin/uploads/brand-certificates",
            headers=headers,
            files={"file": ("certificate.pdf", b"%PDF-1.4", "application/pdf")},
        )
        assert pdf.status_code == 200
        data = pdf.json()["data"]
        assert data["file_key"].endswith(".pdf")
        assert data["file_key"].startswith("files/default/brand-certificates/pending/")
        assert data["file_url"] == data["url"]
        assert data["thumbnail_key"] is None
        assert data["thumbnail_url"] is None
        assert data["mime_type"] == "application/pdf"
        assert data["size"] == 8
        assert data["file_key"] in storage.objects

        image = api_client.post(
            "/api/v1/admin/uploads/brand-certificates",
            headers=headers,
            files={"file": ("certificate.webp", _image_bytes(), "image/webp")},
        )
        assert image.status_code == 200
        image_data = image.json()["data"]
        thumbnail_key = same_directory_thumbnail_object_key(image_data["file_key"])
        assert image_data["file_key"].startswith("images/default/brand-certificates/pending/")
        assert image_data["thumbnail_key"] == thumbnail_key
        assert image_data["thumbnail_url"] == f"/media/{thumbnail_key}"
        assert thumbnail_key.startswith("images/default/brand-certificates/pending/")
        assert image_data["file_key"] in storage.objects
        assert thumbnail_key in storage.objects
        assert storage.objects[thumbnail_key].content != storage.objects[image_data["file_key"]].content

        invalid = api_client.post(
            "/api/v1/admin/uploads/brand-certificates",
            headers=headers,
            files={"file": ("note.txt", b"hello", "text/plain")},
        )
        assert invalid.status_code == 400
        assert invalid.json()["code"] == 50004
    finally:
        set_media_storage_client(None)


def test_brand_certificate_upload_uses_effective_file_limit(api_client: TestClient) -> None:
    storage = InMemoryMediaStorage(objects={})
    set_media_storage_client(storage)
    headers = _admin_headers(api_client)
    try:
        patch = api_client.patch(
            "/api/v1/admin/system-settings/media",
            headers=headers,
            json={"max_file_size_mb": 25},
        )
        assert patch.status_code == 200

        pdf_23m = b"%PDF-1.4\n" + b"x" * (23 * 1024 * 1024)
        accepted = api_client.post(
            "/api/v1/admin/uploads/brand-certificates",
            headers=headers,
            files={"file": ("certificate.pdf", pdf_23m, "application/pdf")},
        )
        assert accepted.status_code == 200
        assert accepted.json()["data"]["file_key"].startswith("files/")

        api_client.patch(
            "/api/v1/admin/system-settings/media",
            headers=headers,
            json={"max_file_size_mb": 1},
        )
        rejected = api_client.post(
            "/api/v1/admin/uploads/brand-certificates",
            headers=headers,
            files={
                "file": (
                    "certificate.pdf",
                    b"%PDF-1.4\n" + b"x" * (2 * 1024 * 1024),
                    "application/pdf",
                )
            },
        )
        assert rejected.status_code == 400
        assert rejected.json()["code"] == 50005
        assert "1MB" in rejected.json()["message"]
    finally:
        set_media_storage_client(None)
