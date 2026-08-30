from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "environment_tiered_evidence.py"
SPEC = importlib.util.spec_from_file_location("environment_tiered_evidence", SCRIPT)
assert SPEC and SPEC.loader
environment_tiered_evidence = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = environment_tiered_evidence
SPEC.loader.exec_module(environment_tiered_evidence)


def write_change(root: Path, change_id: str, body: str) -> Path:
    change_dir = root / "openspec" / "changes" / change_id
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] done\n", encoding="utf-8")
    (change_dir / "acceptance.md").write_text(body, encoding="utf-8")
    return change_dir


def write_sprint(root: Path, sprint_id: str, changes: list[str]) -> None:
    sprint_dir = root / "iterations" / "change" / sprint_id
    sprint_dir.mkdir(parents=True)
    sprint_dir.joinpath("sprint.yaml").write_text(
        "status: in_progress\nchanges:\n" + "".join(f"  - {change}\n" for change in changes),
        encoding="utf-8",
    )


def test_change_blocks_development_evidence_claiming_production_passed(tmp_path: Path) -> None:
    write_change(
        tmp_path,
        "fix-env-claim",
        "DevTools Network 开发环境截图已验证 production 生产环境通过。\n",
    )

    report = environment_tiered_evidence.validate_change(tmp_path, "fix-env-claim")

    assert not report.ok
    assert report.blockers[0].rule_id == "environment-claim-mismatch"


def test_change_blocks_network_pass_without_evidence_ref(tmp_path: Path) -> None:
    write_change(
        tmp_path,
        "fix-network-evidence",
        "source: network_trial\nstatus: passed\n",
    )

    report = environment_tiered_evidence.validate_change(tmp_path, "fix-network-evidence")

    assert not report.ok
    assert report.blockers[0].rule_id == "network-pass-missing-evidence"


def test_production_only_pending_requires_scope_in_development(tmp_path: Path) -> None:
    write_change(
        tmp_path,
        "fix-pending-scope",
        "classification: production_only_pending\nphase: production_publish\n",
    )

    report = environment_tiered_evidence.validate_change(tmp_path, "fix-pending-scope")

    assert not report.ok
    assert report.blockers[0].rule_id == "production-pending-missing-scope"


def test_production_only_pending_blocks_production_release_target(tmp_path: Path) -> None:
    release_dir = tmp_path / "releases" / "v1.0.0"
    release_dir.mkdir(parents=True)
    release_dir.joinpath("release.json").write_text(
        json.dumps(
            {
                "version": "v1.0.0",
                "known_issues": [
                    {
                        "classification": "production_only_pending",
                        "target_environment": "production",
                        "phase": "production_publish",
                        "blocking_scope": "release-publish:production",
                        "evidence_ref": "development archive follow-up",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = environment_tiered_evidence.validate_release(tmp_path, release_dir, target="production")

    assert not report.ok
    assert report.blockers[0].rule_id == "production-pending-at-production-target"


def test_sprint_scans_scoped_change_evidence(tmp_path: Path) -> None:
    write_sprint(tmp_path, "sprint-999", ["fix-env-claim"])
    write_change(
        tmp_path,
        "fix-env-claim",
        "source: real_device\nstatus: passed\nevidence_ref: screenshot-001\n",
    )

    report = environment_tiered_evidence.validate_sprint(tmp_path, "sprint-999")

    assert report.ok
    assert any(path.endswith("acceptance.md") for path in report.checked_files)
