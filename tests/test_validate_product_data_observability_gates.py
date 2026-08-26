from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-product-data-observability-gates.py"

spec = importlib.util.spec_from_file_location("validate_product_data_observability_gates", SCRIPT)
assert spec is not None
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


STANDARD = "docs/standards/product-data-collection-observability.md"
GATE_TEXT = f"""
{STANDARD}
product_data_collection_observability
affected_layers
reason
validation
N/A
"""


def write_minimal_entries(root: Path) -> None:
    for item in validator.ENTRY_FILES + validator.SKILL_FILES:
        path = root / item
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(GATE_TEXT, encoding="utf-8")


def test_missing_entry_reference_is_reported(tmp_path: Path, monkeypatch) -> None:
    write_minimal_entries(tmp_path)
    (tmp_path / "AGENTS.md").write_text("product_data_collection_observability\n", encoding="utf-8")
    monkeypatch.setattr(validator, "ROOT", tmp_path)

    errors = validator.validate_entry_files()

    assert any("AGENTS.md: 缺少采集规范门禁关键内容" in error for error in errors)


def test_change_trigger_without_declaration_is_reported(tmp_path: Path, monkeypatch) -> None:
    write_minimal_entries(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "design.md").write_text("## 设计\n\n修改 API 请求封装和 request_logs。\n", encoding="utf-8")
    monkeypatch.setattr(validator, "ROOT", tmp_path)

    scan = validator.collect_change("fix-demo")
    errors = validator.validate_target(scan)

    assert "change:fix-demo: 命中采集规范触发范围但缺少 `product_data_collection_observability` 声明" in errors


def test_short_na_reason_is_reported(tmp_path: Path, monkeypatch) -> None:
    write_minimal_entries(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "trace.md").write_text(
        """## 声明

```yaml
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 无
  validation: 聚焦校验。
```

涉及 API。
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(validator, "ROOT", tmp_path)

    scan = validator.collect_change("fix-demo")
    errors = validator.validate_target(scan)

    assert "change:fix-demo: N/A 声明缺少可审计 reason" in errors


def test_valid_change_passes(tmp_path: Path, monkeypatch) -> None:
    write_minimal_entries(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "trace.md").write_text(
        """## 声明

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - api
    - request_logs
  reason: 该 Change 修改 API 请求日志字段。
  validation: 运行聚焦校验和 API 回归测试。
```
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(validator, "ROOT", tmp_path)

    assert validator.validate_target(validator.collect_change("fix-demo")) == []


def test_cli_focus_does_not_scan_archive(tmp_path: Path) -> None:
    write_minimal_entries(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "trace.md").write_text(GATE_TEXT + "\n涉及 API。\n", encoding="utf-8")
    archived = tmp_path / "openspec" / "archive" / "2026-01-01-old" / "trace.md"
    archived.parent.mkdir(parents=True)
    archived.write_text("涉及 API 但缺声明。\n", encoding="utf-8")

    result = subprocess.run(
        ["python", str(SCRIPT), "--root", str(tmp_path), "--change", "fix-demo"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "产品数据采集与链路观测门禁校验通过" in result.stdout
