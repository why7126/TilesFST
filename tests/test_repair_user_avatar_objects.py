from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from repair_user_avatar_objects import run_repair  # noqa: E402


def _init_db(db_path: Path) -> None:
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE users (
              id TEXT PRIMARY KEY,
              username TEXT NOT NULL,
              avatar_object_key TEXT,
              updated_at TEXT
            );
            INSERT INTO users (id, username, avatar_object_key, updated_at)
            VALUES
              ('u1', 'admin', 'images/default/user/avatars/missing.png', '2026-08-25T00:00:00Z'),
              ('u2', 'operator', 'images/default/user/avatars/ok.png', '2026-08-25T00:00:00Z'),
              ('u3', 'empty', NULL, '2026-08-25T00:00:00Z');
            """
        )
        connection.commit()
    finally:
        connection.close()


def _avatar_key(db_path: Path, user_id: str) -> str | None:
    connection = sqlite3.connect(db_path)
    try:
        row = connection.execute(
            "SELECT avatar_object_key FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return row[0] if row else None
    finally:
        connection.close()


def test_dry_run_reports_missing_avatar_without_writing(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    _init_db(db_path)

    result = run_repair(
        db_path,
        apply=False,
        exists=lambda key: key.endswith("/ok.png"),
    )

    assert result["mode"] == "dry_run"
    assert result["summary"] == {
        "checked_users": 2,
        "missing_objects": 1,
        "cleared_avatar_keys": 0,
    }
    assert _avatar_key(db_path, "u1") == "images/default/user/avatars/missing.png"
    assert "object_key_hash" in result["items"][0]
    assert "missing.png" not in result["items"][0].values()


def test_apply_clears_missing_avatar_and_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    _init_db(db_path)

    result = run_repair(
        db_path,
        apply=True,
        exists=lambda key: key.endswith("/ok.png"),
    )
    second = run_repair(
        db_path,
        apply=False,
        exists=lambda key: key.endswith("/ok.png"),
    )

    assert result["summary"]["missing_objects"] == 1
    assert result["summary"]["cleared_avatar_keys"] == 1
    assert _avatar_key(db_path, "u1") is None
    assert _avatar_key(db_path, "u2") == "images/default/user/avatars/ok.png"
    assert second["summary"]["missing_objects"] == 0
