from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "archive-change.sh"


def write_minimal_project(root: Path) -> None:
    required_files = [
        "AGENTS.md",
        "README.md",
        "rules/directory-structure.md",
        "openspec/project.md",
        "src/backend/app/main.py",
        "src/web/package.json",
        "src/miniapp/app.json",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        "docker-compose.prod.external.yml",
        "src/backend/Dockerfile",
        "src/web/Dockerfile",
        "src/web/nginx.conf",
    ]
    required_dirs = [
        "rules",
        "docs",
        "openspec",
        "issues",
        "iterations",
        "releases",
        "compatibility",
        ".agents",
        "src",
        "tests",
        "scripts",
        "data",
        "deploy",
    ]
    for item in required_dirs:
        (root / item).mkdir(parents=True, exist_ok=True)
    for item in required_files:
        path = root / item
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")

    scripts_dir = root / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    (scripts_dir / "validate-directory-structure.py").write_text(
        (ROOT / "scripts" / "validate-directory-structure.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (scripts_dir / "archive_evidence.py").write_text(
        (ROOT / "scripts" / "archive_evidence.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (scripts_dir / "validate-archive-evidence.py").write_text(
        (ROOT / "scripts" / "validate-archive-evidence.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (scripts_dir / "validate-openspec-language.py").write_text(
        (ROOT / "scripts" / "validate-openspec-language.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def write_fake_openspec(
    bin_dir: Path,
    extra_stderr: str = "",
    *,
    known_warning_stream: str = "stderr",
    extra_stdout: str = "",
    multiline_warning: bool = False,
) -> None:
    fake = bin_dir / "openspec"
    known_warning = (
        "Proposal warnings in proposal.md\\n"
        "Missing required sections:\\n"
        "  - ## Why\\n"
        "  - ## What Changes"
        if multiline_warning
        else "proposal.md is missing standard ## Why / ## What Changes headings"
    )
    warning_redirect = ">&2" if known_warning_stream == "stderr" else ""
    fake.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "[[ \"$1\" == \"archive\" ]] || exit 64",
                "change_id=\"$2\"",
                "archive_date=\"2026-07-29\"",
                f"echo {known_warning!r} {warning_redirect}".rstrip(),
                *(f"echo {extra_stdout!r}".splitlines() if extra_stdout else []),
                *(f"echo {extra_stderr!r} >&2".splitlines() if extra_stderr else []),
                "mkdir -p \"openspec/changes/archive/${archive_date}-${change_id}\"",
                "mv \"openspec/changes/${change_id}/tasks.md\" \"openspec/changes/archive/${archive_date}-${change_id}/tasks.md\"",
                "mv \"openspec/changes/${change_id}/trace.md\" \"openspec/changes/archive/${archive_date}-${change_id}/trace.md\"",
                "rmdir \"openspec/changes/${change_id}\"",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)


def test_archive_script_relocates_legacy_cli_output(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] 完成归档测试夹具准备。\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")

    bin_dir = tmp_path / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    write_fake_openspec(bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    result = subprocess.run(
        [str(SCRIPT), "fix-demo", "2026-07-29"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert (tmp_path / "openspec" / "archive" / "2026-07-29-fix-demo" / "tasks.md").exists()
    assert (tmp_path / "openspec" / "archive" / "2026-07-29-fix-demo" / "trace.md").exists()
    assert not (tmp_path / "openspec" / "changes" / "archive").exists()
    assert "OpenSpec 文档语言校验通过" in result.stdout
    assert "目录结构校验通过" in result.stdout
    assert "**Evidence Status:** trace-present" in result.stdout
    assert "English scaffold heading compatibility warning" not in result.stderr
    assert "missing standard ## Why / ## What Changes" not in result.stderr


def test_archive_script_preserves_unknown_stderr_with_known_cli_warning(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] 完成归档测试夹具准备。\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")

    bin_dir = tmp_path / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    write_fake_openspec(bin_dir, extra_stderr="unexpected archive warning")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    result = subprocess.run(
        [str(SCRIPT), "fix-demo", "2026-07-29"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "unexpected archive warning" in result.stderr
    assert "missing standard ## Why / ## What Changes" not in result.stderr


def test_archive_script_filters_known_cli_warning_from_stdout(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] 完成归档测试夹具准备。\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")

    bin_dir = tmp_path / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    write_fake_openspec(bin_dir, known_warning_stream="stdout")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    result = subprocess.run(
        [str(SCRIPT), "fix-demo", "2026-07-29"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "missing standard ## Why / ## What Changes" not in result.stdout
    assert "missing standard ## Why / ## What Changes" not in result.stderr


def test_archive_script_preserves_unknown_stdout_with_known_cli_warning(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] 完成归档测试夹具准备。\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")

    bin_dir = tmp_path / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    write_fake_openspec(
        bin_dir,
        known_warning_stream="stdout",
        extra_stdout="unexpected archive stdout",
    )

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    result = subprocess.run(
        [str(SCRIPT), "fix-demo", "2026-07-29"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "unexpected archive stdout" in result.stdout
    assert "missing standard ## Why / ## What Changes" not in result.stdout
    assert "missing standard ## Why / ## What Changes" not in result.stderr


def test_archive_script_filters_multiline_proposal_warning_from_stdout(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] 完成归档测试夹具准备。\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")

    bin_dir = tmp_path / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    write_fake_openspec(bin_dir, known_warning_stream="stdout", multiline_warning=True)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    result = subprocess.run(
        [str(SCRIPT), "fix-demo", "2026-07-29"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "Proposal warnings in proposal.md" not in result.stdout
    assert "Missing required sections" not in result.stdout
    assert "## Why" not in result.stdout
    assert "## What Changes" not in result.stdout


def test_archive_script_language_gate_failure_blocks_before_archive(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    change_dir = tmp_path / "openspec" / "changes" / "fix-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "proposal.md").write_text("## Why\n\nEnglish scaffold.\n", encoding="utf-8")
    (change_dir / "tasks.md").write_text("- [x] 完成归档测试夹具准备。\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n# Trace\n", encoding="utf-8")

    bin_dir = tmp_path / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    write_fake_openspec(bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    result = subprocess.run(
        [str(SCRIPT), "fix-demo", "2026-07-29"],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "OpenSpec 文档语言校验失败" in result.stdout
    assert (tmp_path / "openspec" / "changes" / "fix-demo").exists()
    assert not (tmp_path / "openspec" / "archive" / "2026-07-29-fix-demo").exists()


def test_archive_evidence_cli_auto_generates_minimal_trace(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    archive_dir = tmp_path / "openspec" / "archive" / "2026-07-29-fix-demo"
    archive_dir.mkdir(parents=True)
    (archive_dir / "tasks.md").write_text("- [x] done\n", encoding="utf-8")

    result = subprocess.run(
        [
            "python",
            str(ROOT / "scripts" / "validate-archive-evidence.py"),
            "--change",
            "fix-demo",
            "--archive-path",
            str(archive_dir),
            "--root",
            str(tmp_path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "**Evidence Status:** auto-generated-minimal-trace" in result.stdout
    assert "**Generated Trace:** `openspec/archive/2026-07-29-fix-demo/trace.md`" in result.stdout
    trace = archive_dir / "trace.md"
    assert trace.exists()
    assert "source: auto_generated_minimal_archive_trace" in trace.read_text(encoding="utf-8")


def test_archive_evidence_cli_can_emit_structured_fallback_without_writing(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    archive_dir = tmp_path / "openspec" / "archive" / "2026-07-29-fix-demo"
    archive_dir.mkdir(parents=True)
    (archive_dir / "tasks.md").write_text(
        """- [x] done

## 归档验证摘要

- 验证命令：`pytest tests/test_demo.py`，验证结果：pass。
- 验收结论：通过。
- Issue/Sprint 状态：无关联 Issue，Sprint 不适用。
- 归档路径：openspec/archive/2026-07-29-fix-demo。
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            "python",
            str(ROOT / "scripts" / "validate-archive-evidence.py"),
            "--change",
            "fix-demo",
            "--archive-path",
            str(archive_dir),
            "--root",
            str(tmp_path),
            "--no-write-minimal-trace",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "**Evidence Status:** fallback-summary-pass" in result.stdout
    assert '"evidence_status": "structured-fallback-summary"' in result.stdout
    assert not (archive_dir / "trace.md").exists()


def test_archive_evidence_cli_blocks_missing_trace_and_task_facts(tmp_path: Path) -> None:
    write_minimal_project(tmp_path)
    archive_dir = tmp_path / "openspec" / "archive" / "2026-07-29-fix-demo"
    archive_dir.mkdir(parents=True)
    (archive_dir / "tasks.md").write_text("done without checklist\n", encoding="utf-8")

    result = subprocess.run(
        [
            "python",
            str(ROOT / "scripts" / "validate-archive-evidence.py"),
            "--change",
            "fix-demo",
            "--archive-path",
            str(archive_dir),
            "--root",
            str(tmp_path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "**Verdict:** BLOCKED" in result.stdout
    assert "fix-demo" in result.stdout
    assert "openspec/archive/2026-07-29-fix-demo" in result.stdout
    assert "tasks" in result.stdout
    assert "proposal.md" in result.stdout
