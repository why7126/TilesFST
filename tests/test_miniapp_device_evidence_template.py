from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "standards" / "miniapp-device-evidence-template.md"


def _read_template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def test_miniapp_device_evidence_template_exists_with_core_structure() -> None:
    source = _read_template()

    assert "created_at: 2026-07-19 18:41:32" in source
    assert "updated_at: 2026-07-19 18:41:32" in source
    assert "miniapp_device_evidence:" in source
    for field in ["template_ref", "target", "pages", "evidence_items", "summary"]:
        assert field in source

    for status in [
        "required",
        "passed",
        "failed",
        "blocked",
        "not_applicable",
        "follow_up",
    ]:
        assert f"`{status}`" in source


def test_miniapp_device_evidence_template_covers_device_fields_and_boundaries() -> None:
    source = _read_template()

    for field in [
        "wechat_devtools_version",
        "base_library_version",
        "simulator",
        "device_model",
        "os_version",
        "wechat_version",
        "safe_area_result",
        "touch_result",
        "executor",
        "executed_at",
    ]:
        assert field in source

    assert "DevTools 不等同于真机验收" in source
    assert "静态测试通过 MUST NOT" not in source
    assert "不证明 DevTools 或真机通过" in source
    assert "无真机 evidence 时不得写成真机通过" in source


def test_miniapp_device_evidence_template_covers_security_and_references() -> None:
    source = _read_template()

    for forbidden_term in [
        "本机绝对路径",
        "token",
        "Cookie",
        "Authorization header",
        ".env",
        "真实密钥",
        "数据库 DSN",
        "MinIO 凭据",
        "真实客户数据",
        "未脱敏手机号",
    ]:
        assert forbidden_term in source

    for reference in [
        "REQ `acceptance.md`",
        "OpenSpec `tasks.md`",
        "Change `trace.md` / `acceptance.md`",
        "Sprint `acceptance-report.md`",
        "release note",
        "docs/knowledge-base/retrospectives/sprint-008-retrospective.md",
    ]:
        assert reference in source
