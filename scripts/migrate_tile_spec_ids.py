#!/usr/bin/env python3
"""Match existing tiles.size values to tile_specs and backfill tiles.spec_id.

Usage:
  python scripts/migrate_tile_spec_ids.py --dry-run
  python scripts/migrate_tile_spec_ids.py --apply
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SIZE_PATTERN = re.compile(r"^(\d+)\s*[×xX]\s*(\d+)\s*mm$", re.IGNORECASE)


def default_db_path(project_root: Path) -> Path:
    return project_root / "data" / "sqlite" / "tilesfst.db"


def ensure_tile_specs_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tile_specs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          width_mm INTEGER NOT NULL,
          length_mm INTEGER NOT NULL,
          thickness_mm REAL,
          unit TEXT NOT NULL DEFAULT 'mm',
          display_name TEXT NOT NULL,
          sort_order INTEGER NOT NULL DEFAULT 100,
          status TEXT NOT NULL DEFAULT 'ENABLED',
          sku_count INTEGER NOT NULL DEFAULT 0,
          remark TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          UNIQUE(width_mm, length_mm, unit)
        )
        """
    )
    columns = {row[1] for row in conn.execute("PRAGMA table_info(tiles)").fetchall()}
    if "spec_id" not in columns:
        conn.execute("ALTER TABLE tiles ADD COLUMN spec_id INTEGER")


def find_or_create_spec(
    conn: sqlite3.Connection,
    *,
    width_mm: int,
    length_mm: int,
    apply: bool,
) -> int | None:
    row = conn.execute(
        """
        SELECT id FROM tile_specs
        WHERE width_mm = ? AND length_mm = ? AND unit = 'mm'
        """,
        (width_mm, length_mm),
    ).fetchone()
    if row:
        return int(row[0])
    if not apply:
        return -1
    now = datetime.now(UTC).isoformat()
    display_name = f"{width_mm}×{length_mm}mm"
    cursor = conn.execute(
        """
        INSERT INTO tile_specs (
          width_mm, length_mm, unit, display_name, sort_order, status,
          sku_count, created_at, updated_at
        ) VALUES (?, ?, 'mm', ?, 100, 'ENABLED', 0, ?, ?)
        """,
        (width_mm, length_mm, display_name, now, now),
    )
    return int(cursor.lastrowid)


def rebuild_spec_sku_counts(conn: sqlite3.Connection, *, apply: bool) -> None:
    if not apply:
        return
    conn.execute("UPDATE tile_specs SET sku_count = 0")
    rows = conn.execute(
        """
        SELECT spec_id, COUNT(*) AS c
        FROM tiles
        WHERE spec_id IS NOT NULL
        GROUP BY spec_id
        """
    ).fetchall()
    for spec_id, count in rows:
        conn.execute(
            "UPDATE tile_specs SET sku_count = ? WHERE id = ?",
            (int(count), int(spec_id)),
        )


def migrate(conn: sqlite3.Connection, *, apply: bool) -> tuple[int, int, int]:
    matched = 0
    failed = 0
    skipped = 0
    tiles = conn.execute("SELECT id, size, spec_id FROM tiles").fetchall()
    for tile_id, size, spec_id in tiles:
        if spec_id is not None:
            skipped += 1
            continue
        size_text = (size or "").strip()
        if not size_text:
            failed += 1
            continue

        by_display = conn.execute(
            "SELECT id FROM tile_specs WHERE display_name = ?",
            (size_text,),
        ).fetchone()
        target_spec_id: int | None = int(by_display[0]) if by_display else None

        if target_spec_id is None:
            match = SIZE_PATTERN.match(size_text)
            if match:
                target_spec_id = find_or_create_spec(
                    conn,
                    width_mm=int(match.group(1)),
                    length_mm=int(match.group(2)),
                    apply=apply,
                )
                if target_spec_id == -1:
                    matched += 1
                    continue

        if target_spec_id is None or target_spec_id <= 0:
            failed += 1
            continue

        matched += 1
        if apply:
            conn.execute(
                "UPDATE tiles SET spec_id = ? WHERE id = ?",
                (target_spec_id, tile_id),
            )

    rebuild_spec_sku_counts(conn, apply=apply)
    if apply:
        conn.commit()
    return matched, failed, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill tiles.spec_id from tiles.size")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    parser.add_argument("--db", type=Path, default=default_db_path(PROJECT_ROOT))
    args = parser.parse_args()

    if not args.db.exists():
        print(f"Database not found: {args.db}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(args.db)
    try:
        ensure_tile_specs_table(conn)
        matched, failed, skipped = migrate(conn, apply=args.apply)
        mode = "APPLY" if args.apply else "DRY-RUN"
        print(f"[{mode}] matched={matched} failed={failed} skipped={skipped}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
