from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-openspec-language.py"


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(SCRIPT), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_blocks_english_scaffold_headings_and_tasks(tmp_path: Path) -> None:
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text(
        """## 1. Implementation

- [x] Run pytest tests/test_demo.py
""",
        encoding="utf-8",
    )

    result = run_validator(tmp_path)

    assert result.returncode == 1
    assert "OpenSpec 文档语言校验失败" in result.stdout
    assert "Implementation" in result.stdout
    assert "Run pytest" in result.stdout


def test_allows_chinese_first_tasks_with_commands(tmp_path: Path) -> None:
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text(
        """## 1. 实现

- [x] 运行 `pytest tests/test_demo.py` 并记录结果。
- [ ] 验证 API 字段 `brand_logo_url` 保持兼容。
""",
        encoding="utf-8",
    )

    result = run_validator(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OpenSpec 文档语言校验通过" in result.stdout


def test_ignores_code_fences(tmp_path: Path) -> None:
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "design.md").write_text(
        """## 设计

```markdown
## Implementation
- [x] Run pytest
```
""",
        encoding="utf-8",
    )

    result = run_validator(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
