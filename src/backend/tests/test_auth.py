"""Auth API integration tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AuthInvalidCredentialsError
from app.db.seed import DEFAULT_ADMIN_USERNAME, seed_admin_user
from app.db.session import get_db, get_session_factory, init_database, reset_engine
from app.main import app
from app.modules.media.storage import StoredMediaObject, set_media_storage_client
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


class InMemoryMediaStorageClient:
    def __init__(self) -> None:
        self.objects: dict[str, StoredMediaObject] = {}
        self.put_calls: list[tuple[str, str | None]] = []
        self.fail_put = False

    def put_object(self, object_key: str, content: bytes, content_type: str | None) -> None:
        if self.fail_put:
            from app.core.error_codes import STORAGE_UNAVAILABLE
            from app.core.exceptions import AppError

            raise AppError(status_code=502, code=STORAGE_UNAVAILABLE, message="对象存储不可用")
        self.put_calls.append((object_key, content_type))
        self.objects[object_key] = StoredMediaObject(content=content, content_type=content_type)

    def get_object(self, object_key: str) -> StoredMediaObject:
        try:
            return self.objects[object_key]
        except KeyError as exc:
            from app.core.exceptions import AppError
            from app.modules.media.storage import MEDIA_NOT_FOUND

            raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体文件不存在") from exc


@pytest.fixture()
def client(tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    db_path = tmp_path / "test.db"
    media_storage = InMemoryMediaStorageClient()
    monkeypatch.setenv("SQLITE_DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("MINIO_BUCKET", "tile-info-platform")
    monkeypatch.setenv("ADMIN_INITIAL_PASSWORD", "AdminPass123!")
    monkeypatch.setenv("APP_SECRET_KEY", "test-secret-key")
    reset_engine()
    settings.sqlite_database_url = f"sqlite:///{db_path}"
    settings.minio_bucket = "tile-info-platform"
    settings.admin_username = DEFAULT_ADMIN_USERNAME
    settings.admin_initial_password = "AdminPass123!"
    settings.admin_reset_password_on_startup = False
    settings.app_secret_key = "test-secret-key"
    set_media_storage_client(media_storage)
    init_database()

    session = get_session_factory()()
    from app.db.seed import seed_admin_user

    seed_admin_user(session)

    def override_get_db() -> Generator[Session, None, None]:
        db = get_session_factory()()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    set_media_storage_client(None)
    reset_engine()


def _login(client: TestClient, username: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password, "remember_me": False},
    )
    assert response.status_code == 200
    return response.json()["data"]


def _prepare_seed_database(
    tmp_path,
    monkeypatch,
    *,
    password: str = "AdminPass123!",
    reset_on_startup: bool = False,
) -> None:
    db_path = tmp_path / "seed.db"
    monkeypatch.setenv("SQLITE_DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
    monkeypatch.setenv("ADMIN_INITIAL_PASSWORD", password)
    monkeypatch.setenv("ADMIN_RESET_PASSWORD_ON_STARTUP", str(reset_on_startup).lower())
    monkeypatch.setenv("APP_SECRET_KEY", "test-secret-key")
    reset_engine()
    settings.sqlite_database_url = f"sqlite:///{db_path}"
    settings.admin_username = DEFAULT_ADMIN_USERNAME
    settings.admin_initial_password = password
    settings.admin_reset_password_on_startup = reset_on_startup
    settings.app_secret_key = "test-secret-key"
    init_database()


def _login_with_auth_service(username: str, password: str) -> None:
    session = get_session_factory()()
    try:
        service = AuthService(UserRepository(session))
        service.login(username=username, password=password, remember_me=False)
    finally:
        session.close()


def _admin_password_hash() -> str:
    session = get_session_factory()()
    try:
        row = session.execute(
            text("SELECT password_hash FROM users WHERE username = :username"),
            {"username": DEFAULT_ADMIN_USERNAME},
        ).mappings().one()
        return str(row["password_hash"])
    finally:
        session.close()


def test_seed_creates_default_admin_from_initial_password(tmp_path, monkeypatch) -> None:
    _prepare_seed_database(tmp_path, monkeypatch, password="InitialPass123!")

    session = get_session_factory()()
    try:
        assert seed_admin_user(session) is True
    finally:
        session.close()

    _login_with_auth_service(DEFAULT_ADMIN_USERNAME, "InitialPass123!")


def test_seed_existing_admin_repeat_startup_keeps_password_hash(tmp_path, monkeypatch) -> None:
    _prepare_seed_database(tmp_path, monkeypatch, password="InitialPass123!")
    session = get_session_factory()()
    try:
        assert seed_admin_user(session) is True
    finally:
        session.close()
    original_hash = _admin_password_hash()

    session = get_session_factory()()
    try:
        assert seed_admin_user(session) is False
    finally:
        session.close()

    assert _admin_password_hash() == original_hash
    _login_with_auth_service(DEFAULT_ADMIN_USERNAME, "InitialPass123!")


def test_seed_initial_password_change_without_reset_does_not_overwrite(
    tmp_path,
    monkeypatch,
) -> None:
    _prepare_seed_database(tmp_path, monkeypatch, password="InitialPass123!")
    session = get_session_factory()()
    try:
        seed_admin_user(session)
    finally:
        session.close()
    original_hash = _admin_password_hash()

    settings.admin_initial_password = "ChangedPass123!"
    settings.admin_reset_password_on_startup = False
    session = get_session_factory()()
    try:
        assert seed_admin_user(session) is False
    finally:
        session.close()

    assert _admin_password_hash() == original_hash
    _login_with_auth_service(DEFAULT_ADMIN_USERNAME, "InitialPass123!")
    with pytest.raises(AuthInvalidCredentialsError):
        _login_with_auth_service(DEFAULT_ADMIN_USERNAME, "ChangedPass123!")


def test_seed_explicit_reset_updates_admin_password(tmp_path, monkeypatch) -> None:
    _prepare_seed_database(tmp_path, monkeypatch, password="InitialPass123!")
    session = get_session_factory()()
    try:
        seed_admin_user(session)
    finally:
        session.close()
    original_hash = _admin_password_hash()

    settings.admin_initial_password = "RecoveredPass123!"
    settings.admin_reset_password_on_startup = True
    session = get_session_factory()()
    try:
        assert seed_admin_user(session) is True
    finally:
        session.close()

    assert _admin_password_hash() != original_hash
    _login_with_auth_service(DEFAULT_ADMIN_USERNAME, "RecoveredPass123!")
    with pytest.raises(AuthInvalidCredentialsError):
        _login_with_auth_service(DEFAULT_ADMIN_USERNAME, "InitialPass123!")


def test_login_success(client: TestClient) -> None:
    data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    assert data["token_type"] == "Bearer"
    assert data["user"]["role"] == "admin"
    assert data["access_token"]


def test_login_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": DEFAULT_ADMIN_USERNAME, "password": "wrong-password", "remember_me": False},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["code"] == 40101
    assert body["message"] == "账号或密码错误"


def test_login_disabled_user(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        repo.create_user(
            username="disabled-user",
            password="Disabled123!",
            display_name="Disabled User",
            role="employee",
            status="disabled",
        )
    finally:
        session.close()

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "disabled-user", "password": "Disabled123!", "remember_me": False},
    )
    assert response.status_code == 403
    assert response.json()["code"] == 40301


def test_me_with_valid_token(client: TestClient) -> None:
    login_data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["username"] == DEFAULT_ADMIN_USERNAME


def test_me_with_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401
    assert response.json()["code"] == 40102


def test_logout(client: TestClient) -> None:
    login_data = _login(client, DEFAULT_ADMIN_USERNAME, "AdminPass123!")
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["success"] is True


def test_store_owner_rejected_from_admin_api(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        repo = UserRepository(session)
        repo.create_user(
            username="store-owner",
            password="OwnerPass123!",
            display_name="Store Owner",
            role="store_owner",
        )
    finally:
        session.close()

    login_data = _login(client, "store-owner", "OwnerPass123!")
    response = client.post(
        "/api/v1/admin/tiles",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
        json={"name": "测试砖", "model": "T-001", "category": "地砖"},
    )
    assert response.status_code == 403
    assert response.json()["code"] == 40302
