"""Lightweight SQLite migrations applied after schema.sql."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Connection


def _users_table_sql(connection: Connection) -> str:
    row = connection.execute(
        text("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
    ).scalar_one_or_none()
    return row or ""


def _column_names(connection: Connection, table: str) -> set[str]:
    rows = connection.execute(text(f"PRAGMA table_info({table})")).fetchall()
    return {row[1] for row in rows}


def apply_migrations(connection: Connection) -> None:
    users_sql = _users_table_sql(connection)
    if not users_sql:
        return

    needs_rebuild = "deleted" not in users_sql or "avatar_object_key" not in users_sql
    if needs_rebuild:
        _rebuild_users_table(connection)
        return

    columns = _column_names(connection, "users")
    if "avatar_object_key" not in columns:
        connection.execute(text("ALTER TABLE users ADD COLUMN avatar_object_key TEXT"))


def _rebuild_users_table(connection: Connection) -> None:
    connection.execute(text("PRAGMA foreign_keys=OFF"))
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS users_new (
              id TEXT PRIMARY KEY,
              username TEXT NOT NULL UNIQUE,
              phone TEXT,
              email TEXT,
              password_hash TEXT NOT NULL,
              display_name TEXT,
              role TEXT NOT NULL CHECK (role IN ('admin', 'employee', 'store_owner')),
              status TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'disabled', 'deleted')),
              avatar_object_key TEXT,
              last_login_at TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
    )
    old_columns = _column_names(connection, "users")
    avatar_select = (
        "avatar_object_key" if "avatar_object_key" in old_columns else "NULL AS avatar_object_key"
    )
    connection.execute(
        text(
            f"""
            INSERT INTO users_new (
              id, username, phone, email, password_hash, display_name,
              role, status, avatar_object_key, last_login_at, created_at, updated_at
            )
            SELECT
              id, username, phone, email, password_hash, display_name,
              role, status, {avatar_select}, last_login_at, created_at, updated_at
            FROM users
            """
        )
    )
    connection.execute(text("DROP TABLE users"))
    connection.execute(text("ALTER TABLE users_new RENAME TO users"))
    connection.execute(text("PRAGMA foreign_keys=ON"))
