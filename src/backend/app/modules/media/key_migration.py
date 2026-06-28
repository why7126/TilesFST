"""Legacy object key mapping for REQ-0012 migration."""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

MEDIA_OBJECT_KEY_QUERIES: tuple[tuple[str, str], ...] = (
    ("users", "avatar_object_key"),
    ("brands", "logo_object_key"),
    ("tile_images", "object_key"),
    ("tile_videos", "object_key"),
)

_OLD_AVATAR = re.compile(r"^original/default/avatars/\d{4}/\d{2}/(?P<filename>.+)$")
_OLD_BRAND_LOGO = re.compile(r"^original/default/brands/logos/\d{4}/\d{2}/(?P<filename>.+)$")
_OLD_TILE_IMAGE = re.compile(
    r"^original/default/tiles/(?P<tile>[^/]+)/images/\d{4}/\d{2}/(?P<filename>.+)$"
)
_OLD_TILE_VIDEO = re.compile(
    r"^videos/default/tiles/(?P<tile>[^/]+)/\d{4}/\d{2}/(?P<filename>.+)$"
)


@dataclass(frozen=True)
class KeyMigration:
    table: str
    column: str
    row_id: int
    old_key: str
    new_key: str


def map_legacy_object_key(old_key: str) -> str | None:
    """Return new key for legacy layout, or None if already current / unrecognized."""
    key = old_key.strip().lstrip("/")
    if not key:
        return None

    if match := _OLD_AVATAR.match(key):
        return f"images/default/user/avatars/{match.group('filename')}"
    if match := _OLD_BRAND_LOGO.match(key):
        return f"images/default/brands/logos/{match.group('filename')}"
    if match := _OLD_TILE_IMAGE.match(key):
        return f"images/default/tiles/{match.group('tile')}/{match.group('filename')}"
    if match := _OLD_TILE_VIDEO.match(key):
        return f"videos/default/tiles/{match.group('tile')}/{match.group('filename')}"

    return None


def collect_migrations(db_path: Path) -> list[KeyMigration]:
    if not db_path.is_file():
        return []

    migrations: list[KeyMigration] = []
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        for table, column in MEDIA_OBJECT_KEY_QUERIES:
            try:
                rows = connection.execute(
                    f"SELECT rowid AS _rowid, {column} FROM {table} "
                    f"WHERE {column} IS NOT NULL AND TRIM({column}) != ''"
                ).fetchall()
            except sqlite3.OperationalError:
                continue
            for row in rows:
                old_key = str(row[column]).strip()
                new_key = map_legacy_object_key(old_key)
                if new_key is None or new_key == old_key:
                    continue
                migrations.append(
                    KeyMigration(
                        table=table,
                        column=column,
                        row_id=int(row["_rowid"]),
                        old_key=old_key,
                        new_key=new_key,
                    )
                )
    finally:
        connection.close()
    return migrations
