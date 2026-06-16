"""Database session and initialization."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.migrations import apply_migrations

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def _sqlite_path(database_url: str) -> Path | None:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return None
    raw = database_url[len(prefix) :]
    if raw.startswith("/"):
        return Path(raw)
    return Path(raw)


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        db_path = _sqlite_path(settings.sqlite_database_url)
        if db_path is not None:
            db_path.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            settings.sqlite_database_url,
            connect_args={"check_same_thread": False},
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
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in schema_sql.split(";"):
            chunk = statement.strip()
            if chunk:
                connection.execute(text(chunk))
        apply_migrations(connection)


def reset_engine() -> None:
    """Reset cached engine (for tests)."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
