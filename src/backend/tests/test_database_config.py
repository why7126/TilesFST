"""Database configuration and dialect selection tests."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from app.core.config import settings
from app.db import session as db_session
from app.db.seed import seed_admin_user
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


@pytest.fixture(autouse=True)
def reset_database_settings() -> Iterator[None]:
    original = {
        "app_env": settings.app_env,
        "database_url": settings.database_url,
        "sqlite_database_url": settings.sqlite_database_url,
        "admin_username": settings.admin_username,
        "admin_initial_password": settings.admin_initial_password,
        "admin_reset_password_on_startup": settings.admin_reset_password_on_startup,
        "app_secret_key": settings.app_secret_key,
    }
    db_session.reset_engine()
    yield
    db_session.reset_engine()
    for key, value in original.items():
        setattr(settings, key, value)


def test_production_requires_database_url() -> None:
    settings.app_env = "production"
    settings.database_url = None

    with pytest.raises(db_session.DatabaseConfigurationError) as excinfo:
        db_session._resolve_database_url()

    assert "requires a MySQL DATABASE_URL" in str(excinfo.value)


def test_production_rejects_sqlite_database_url_without_password_leak() -> None:
    settings.app_env = "production"
    settings.database_url = "sqlite:////tmp/tilesfst.db"

    with pytest.raises(db_session.DatabaseConfigurationError) as excinfo:
        db_session._resolve_database_url()

    assert "requires a MySQL DATABASE_URL" in str(excinfo.value)
    assert "password" not in str(excinfo.value).lower()


def test_non_production_falls_back_to_sqlite_url() -> None:
    settings.app_env = "development"
    settings.database_url = None
    settings.sqlite_database_url = "sqlite:////tmp/tilesfst-dev.db"

    assert db_session._resolve_database_url() == "sqlite:////tmp/tilesfst-dev.db"


def test_mysql_engine_options_do_not_include_sqlite_connect_args() -> None:
    options = db_session._engine_options(
        "mysql+pymysql://tiles_user:secret@example.com:3306/tiles?charset=utf8mb4"
    )

    assert options["pool_pre_ping"] is True
    assert options["connect_args"] == {"charset": "utf8mb4"}
    assert "check_same_thread" not in options["connect_args"]


@pytest.mark.mysql
def test_mysql_schema_seed_and_login_when_database_url_is_provided() -> None:
    database_url = os.getenv("MYSQL_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("MYSQL_TEST_DATABASE_URL is not configured")

    settings.app_env = "production"
    settings.database_url = database_url
    settings.admin_username = "codex_mysql_admin"
    settings.admin_initial_password = "AdminPass123!"
    settings.admin_reset_password_on_startup = True
    settings.app_secret_key = "test-secret-key"

    db_session.init_database()
    session = db_session.get_session_factory()()
    try:
        seed_admin_user(session)
        service = AuthService(UserRepository(session))
        login = service.login(
            username=settings.admin_username,
            password=settings.admin_initial_password,
            remember_me=False,
        )
    finally:
        session.close()

    assert login.user.username == settings.admin_username
    assert login.access_token
