from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_opsx_apply_skill_declares_admin_filter_dropdown_gate() -> None:
    skill = (ROOT / ".agents" / "skills" / "opsx-apply" / "SKILL.md").read_text(encoding="utf-8")

    assert "`admin-filter-dropdown`" in skill
    assert "AdminFilterSelect" in skill
    assert "SearchableSelect" in skill
    assert "page-local overlay CSS absence" in skill
    assert "overlay clipping check" in skill
    assert "query parameter semantics" in skill
    assert "regression test plan" in skill
    assert "MAY mark the checklist `n/a`" in skill


def test_admin_list_best_practice_contains_filter_dropdown_apply_checklist() -> None:
    best_practice = (
        ROOT / "docs" / "knowledge-base" / "best-practices" / "admin-list-page-consistency.md"
    ).read_text(encoding="utf-8")

    assert "Apply 前必读 Gate" in best_practice
    assert "`admin-filter-dropdown`" in best_practice
    assert "`AdminFilterSelect`" in best_practice
    assert "`SearchableSelect`" in best_practice
    assert "`best-practice read`" in best_practice
    assert "`shared component reuse`" in best_practice
    assert "`overlay clipping`" in best_practice
    assert "`query semantics`" in best_practice
    assert "`regression test plan`" in best_practice
