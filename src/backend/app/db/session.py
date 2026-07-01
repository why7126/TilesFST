"""Database session and initialization."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.migrations import apply_migrations

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
MYSQL_SCHEMA_PATH = Path(__file__).resolve().parent / "schema.mysql.sql"
MYSQL_BASELINE_VERSION = "mysql_baseline_v1"


class DatabaseConfigurationError(RuntimeError):
    """Raised when database environment settings are not deployable."""


def _sqlite_path(database_url: str) -> Path | None:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return None
    raw = database_url[len(prefix) :]
    if raw.startswith("/"):
        return Path(raw)
    return Path(raw)


def _masked_database_url(database_url: str) -> str:
    try:
        return make_url(database_url).render_as_string(hide_password=True)
    except ArgumentError:
        return "<invalid database url>"


def _resolve_database_url() -> str:
    app_env = settings.app_env.strip().lower()
    if app_env == "production":
        if not settings.database_url:
            raise DatabaseConfigurationError(
                "APP_ENV=production requires a MySQL DATABASE_URL."
            )
        try:
            url = make_url(settings.database_url)
        except ArgumentError as exc:
            raise DatabaseConfigurationError("DATABASE_URL is not a valid SQLAlchemy URL.") from exc
        if url.get_backend_name() != "mysql":
            safe_url = url.render_as_string(hide_password=True)
            raise DatabaseConfigurationError(
                f"APP_ENV=production requires a MySQL DATABASE_URL, got {safe_url}."
            )
        return settings.database_url
    return settings.database_url or settings.sqlite_database_url


def _database_backend(database_url: str) -> str:
    try:
        return make_url(database_url).get_backend_name()
    except ArgumentError as exc:
        raise DatabaseConfigurationError(
            f"Database URL is invalid: {_masked_database_url(database_url)}"
        ) from exc


def _engine_options(database_url: str) -> dict:
    backend = _database_backend(database_url)
    if backend == "sqlite":
        return {"connect_args": {"check_same_thread": False}}
    if backend == "mysql":
        return {
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
            "pool_recycle": 1800,
            "connect_args": {"charset": "utf8mb4"},
        }
    raise DatabaseConfigurationError(
        f"Unsupported database dialect for {settings.app_env}: {_masked_database_url(database_url)}"
    )


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        database_url = _resolve_database_url()
        db_path = _sqlite_path(database_url)
        if db_path is not None:
            db_path.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            database_url,
            **_engine_options(database_url),
        )
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def init_database() -> None:
    engine = get_engine()
    backend = engine.dialect.name
    with engine.begin() as connection:
        if backend == "mysql":
            _init_mysql_schema(connection)
        elif backend == "sqlite":
            schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
            for statement in schema_sql.split(";"):
                chunk = statement.strip()
                if chunk:
                    connection.execute(text(chunk))
            apply_migrations(connection)
        else:
            raise DatabaseConfigurationError(f"Unsupported database dialect: {backend}")


def _init_mysql_schema(connection) -> None:
    schema_sql = MYSQL_SCHEMA_PATH.read_text(encoding="utf-8")
    for statement in schema_sql.split(";"):
        chunk = statement.strip()
        if chunk:
            connection.exec_driver_sql(chunk)
    connection.exec_driver_sql(
        """
        INSERT IGNORE INTO schema_migrations (version, applied_at)
        VALUES (%s, UTC_TIMESTAMP(3))
        """,
        (MYSQL_BASELINE_VERSION,),
    )


def reset_engine() -> None:
    """Reset cached engine (for tests)."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
