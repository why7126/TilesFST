from __future__ import annotations

import sys
import importlib.util
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_validator() -> ModuleType:
    module_path = ROOT / "scripts" / "validate-directory-structure.py"
    spec = importlib.util.spec_from_file_location("validate_directory_structure", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def write_required_paths(root: Path) -> None:
    for item in validator.REQUIRED_PATHS:
        path = root / item
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")


def write_allowed_root_dirs(root: Path) -> None:
    for item in validator.ALLOWED_ROOT_DIRS:
        (root / item).mkdir(parents=True, exist_ok=True)


def test_validate_rejects_legacy_openspec_change_archive_root(tmp_path: Path) -> None:
    write_required_paths(tmp_path)
    write_allowed_root_dirs(tmp_path)
    (tmp_path / "openspec" / "changes" / "archive").mkdir(parents=True)

    errors = validator.validate(tmp_path)

    assert any("openspec/changes/archive" in error for error in errors)
