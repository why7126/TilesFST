from __future__ import annotations

from pathlib import Path


def resolve_change_file(root: Path, change_id: str, relative_path: str) -> Path:
    """Resolve a file from an active or archived OpenSpec Change."""

    active_path = root / "openspec" / "changes" / change_id / relative_path
    if active_path.exists():
        return active_path

    archive_root = root / "openspec" / "changes" / "archive"
    archived_matches = sorted(archive_root.glob(f"*-{change_id}/{relative_path}"))
    if archived_matches:
        return archived_matches[-1]

    raise FileNotFoundError(
        f"Change file not found for {change_id}: {relative_path} "
        f"(checked active path and {archive_root}/*-{change_id})"
    )
