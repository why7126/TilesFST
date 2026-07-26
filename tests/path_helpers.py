from __future__ import annotations

from pathlib import Path


def resolve_change_file(root: Path, change_id: str, relative_path: str) -> Path:
    """Resolve a file from an active or archived OpenSpec Change."""

    active_path = root / "openspec" / "changes" / change_id / relative_path
    if active_path.exists():
        return active_path

    checked_roots = [
        root / "openspec" / "archive",
        root / "openspec" / "changes" / "archive",
    ]
    for archive_root in checked_roots:
        archived_matches = sorted(archive_root.glob(f"*-{change_id}/{relative_path}"))
        if archived_matches:
            return archived_matches[-1]

    raise FileNotFoundError(
        f"Change file not found for {change_id}: {relative_path} "
        f"(checked active path and "
        f"{', '.join(str(root / f'*-{change_id}') for root in checked_roots)})"
    )
