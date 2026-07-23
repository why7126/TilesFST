from __future__ import annotations

from pathlib import Path

import pytest

from path_helpers import resolve_change_file


def test_resolve_change_file_prefers_active_path(tmp_path: Path) -> None:
    active = tmp_path / "openspec" / "changes" / "add-demo" / "implementation" / "evidence.md"
    active.parent.mkdir(parents=True)
    active.write_text("active", encoding="utf-8")
    archived = tmp_path / "openspec" / "changes" / "archive" / "2026-07-22-add-demo" / "implementation" / "evidence.md"
    archived.parent.mkdir(parents=True)
    archived.write_text("archived", encoding="utf-8")

    assert resolve_change_file(tmp_path, "add-demo", "implementation/evidence.md") == active


def test_resolve_change_file_falls_back_to_latest_archive(tmp_path: Path) -> None:
    older = tmp_path / "openspec" / "changes" / "archive" / "2026-07-21-add-demo" / "implementation" / "evidence.md"
    older.parent.mkdir(parents=True)
    older.write_text("older", encoding="utf-8")
    newer = tmp_path / "openspec" / "changes" / "archive" / "2026-07-22-add-demo" / "implementation" / "evidence.md"
    newer.parent.mkdir(parents=True)
    newer.write_text("newer", encoding="utf-8")

    assert resolve_change_file(tmp_path, "add-demo", "implementation/evidence.md") == newer


def test_resolve_change_file_reports_checked_paths(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError) as exc_info:
        resolve_change_file(tmp_path, "add-demo", "implementation/evidence.md")

    message = str(exc_info.value)
    assert "add-demo" in message
    assert "implementation/evidence.md" in message
    assert "archive" in message
