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


def _table_exists(connection: Connection, table: str) -> bool:
    row = connection.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:table"),
        {"table": table},
    ).scalar_one_or_none()
    return row is not None


def _ensure_brands_table(connection: Connection) -> None:
    if _table_exists(connection, "brands"):
        return
    connection.execute(
        text(
            """
            CREATE TABLE brands (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              sort_order INTEGER NOT NULL,
              short_name TEXT,
              english_name TEXT,
              logo_object_key TEXT,
              description TEXT,
              status TEXT NOT NULL DEFAULT 'ENABLED'
                CHECK (status IN ('ENABLED', 'DISABLED')),
              sku_count INTEGER NOT NULL DEFAULT 0 CHECK (sku_count >= 0),
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
    )


def apply_migrations(connection: Connection) -> None:
    users_sql = _users_table_sql(connection)
    if not users_sql:
        return

    needs_rebuild = "deleted" not in users_sql or "avatar_object_key" not in users_sql
    if needs_rebuild:
        _rebuild_users_table(connection)

    columns = _column_names(connection, "users")
    if "avatar_object_key" not in columns:
        connection.execute(text("ALTER TABLE users ADD COLUMN avatar_object_key TEXT"))

    _ensure_brands_table(connection)
    _ensure_tile_categories_extended(connection)
    _ensure_tiles_sku_extended(connection)


def _tile_categories_table_sql(connection: Connection) -> str:
    row = connection.execute(
        text("SELECT sql FROM sqlite_master WHERE type='table' AND name='tile_categories'")
    ).scalar_one_or_none()
    return row or ""


def _ensure_tile_categories_extended(connection: Connection) -> None:
    sql = _tile_categories_table_sql(connection)
    if not sql:
        return
    if "parent_id" in sql and "code" in sql:
        return
    _rebuild_tile_categories_table(connection)


def _rebuild_tile_categories_table(connection: Connection) -> None:
    from datetime import UTC, datetime

    now = datetime.now(UTC).isoformat()
    connection.execute(text("PRAGMA foreign_keys=OFF"))
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS tile_categories_new (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              parent_id INTEGER,
              name TEXT NOT NULL,
              code TEXT NOT NULL UNIQUE,
              sort_order INTEGER NOT NULL,
              level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 3),
              description TEXT,
              status TEXT NOT NULL DEFAULT 'ENABLED'
                CHECK (status IN ('ENABLED', 'DISABLED')),
              sku_count INTEGER NOT NULL DEFAULT 0 CHECK (sku_count >= 0),
              path TEXT NOT NULL,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              FOREIGN KEY(parent_id) REFERENCES tile_categories_new(id)
            )
            """
        )
    )
    old_columns = _column_names(connection, "tile_categories")
    if old_columns:
        rows = connection.execute(text("SELECT id, name FROM tile_categories")).fetchall()
        for row in rows:
            cat_id = int(row[0])
            name = row[1]
            code = f"CAT-{cat_id:04d}"
            connection.execute(
                text(
                    """
                    INSERT INTO tile_categories_new (
                      id, parent_id, name, code, sort_order, level, description,
                      status, sku_count, path, created_at, updated_at
                    ) VALUES (
                      :id, NULL, :name, :code, :sort_order, 1, NULL,
                      'ENABLED', 0, :path, :created_at, :updated_at
                    )
                    """
                ),
                {
                    "id": cat_id,
                    "name": name,
                    "code": code,
                    "sort_order": cat_id * 10,
                    "path": name,
                    "created_at": now,
                    "updated_at": now,
                },
            )
    connection.execute(text("DROP TABLE tile_categories"))
    connection.execute(text("ALTER TABLE tile_categories_new RENAME TO tile_categories"))
    connection.execute(text("PRAGMA foreign_keys=ON"))


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


def _tiles_table_sql(connection: Connection) -> str:
    row = connection.execute(
        text("SELECT sql FROM sqlite_master WHERE type='table' AND name='tiles'")
    ).scalar_one_or_none()
    return row or ""


def _ensure_tiles_sku_extended(connection: Connection) -> None:
    sql = _tiles_table_sql(connection)
    if not sql:
        return
    if "sku_code" in sql and "brand_id" in sql:
        _ensure_tile_videos_table(connection)
        return
    _rebuild_tiles_sku_table(connection)
    _ensure_tile_videos_table(connection)


def _ensure_tile_videos_table(connection: Connection) -> None:
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS tile_videos (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              tile_id INTEGER NOT NULL,
              object_key TEXT NOT NULL,
              file_name TEXT NOT NULL,
              file_size_bytes INTEGER,
              duration_seconds REAL,
              sort_order INTEGER NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL,
              FOREIGN KEY(tile_id) REFERENCES tiles(id)
            )
            """
        )
    )


def _rebuild_tiles_sku_table(connection: Connection) -> None:
    from datetime import UTC, datetime

    now = datetime.now(UTC).isoformat()
    connection.execute(text("PRAGMA foreign_keys=OFF"))

    default_brand_id = connection.execute(text("SELECT id FROM brands ORDER BY id LIMIT 1")).scalar()
    default_category_id = connection.execute(
        text("SELECT id FROM tile_categories ORDER BY id LIMIT 1")
    ).scalar()

    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS tiles_new (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              sku_code TEXT NOT NULL UNIQUE,
              brand_id INTEGER NOT NULL,
              category_id INTEGER NOT NULL,
              size TEXT NOT NULL,
              surface_finish TEXT NOT NULL,
              color_family TEXT,
              reference_price REAL,
              remark TEXT,
              status TEXT NOT NULL DEFAULT 'DRAFT'
                CHECK (status IN ('PUBLISHED', 'DRAFT', 'NEEDS_COMPLETION', 'DISABLED')),
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              FOREIGN KEY(brand_id) REFERENCES brands(id),
              FOREIGN KEY(category_id) REFERENCES tile_categories(id)
            )
            """
        )
    )

    old_columns = _column_names(connection, "tiles")
    if old_columns and default_brand_id and default_category_id:
        rows = connection.execute(text("SELECT * FROM tiles")).mappings().all()
        for row in rows:
            row_dict = dict(row)
            old_status = str(row_dict.get("status") or "draft").upper()
            if old_status == "DRAFT" or old_status == "DRAFT":
                status = "DRAFT"
            elif old_status == "PUBLISHED":
                status = "PUBLISHED"
            else:
                status = "DRAFT"
            sku_code = row_dict.get("sku_code") or row_dict.get("model") or f"SKU-MIG-{row_dict['id']}"
            connection.execute(
                text(
                    """
                    INSERT INTO tiles_new (
                      id, name, sku_code, brand_id, category_id, size, surface_finish,
                      color_family, reference_price, remark, status, created_at, updated_at
                    ) VALUES (
                      :id, :name, :sku_code, :brand_id, :category_id, :size, :surface_finish,
                      :color_family, :reference_price, :remark, :status, :created_at, :updated_at
                    )
                    """
                ),
                {
                    "id": row_dict["id"],
                    "name": row_dict["name"],
                    "sku_code": sku_code,
                    "brand_id": default_brand_id,
                    "category_id": row_dict.get("category_id") or default_category_id,
                    "size": row_dict.get("size") or "-",
                    "surface_finish": "-",
                    "color_family": row_dict.get("color"),
                    "reference_price": None,
                    "remark": row_dict.get("description"),
                    "status": status,
                    "created_at": row_dict.get("created_at") or now,
                    "updated_at": row_dict.get("updated_at") or now,
                },
            )

    connection.execute(text("DROP TABLE tiles"))
    connection.execute(text("ALTER TABLE tiles_new RENAME TO tiles"))
    connection.execute(text("PRAGMA foreign_keys=ON"))
