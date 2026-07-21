from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEST_PRACTICE = (
    ROOT / "docs" / "knowledge-base" / "best-practices" / "miniapp-custom-navigation.md"
)
README = ROOT / "docs" / "knowledge-base" / "README.md"


def _read_best_practice() -> str:
    return BEST_PRACTICE.read_text(encoding="utf-8")


def test_miniapp_custom_navigation_best_practice_exists_with_core_sections() -> None:
    source = _read_best_practice()

    assert "created_at: 2026-07-19 20:06:00" in source
    assert "updated_at: 2026-07-19 20:06:00" in source
    for heading in [
        "## 适用范围",
        "## 导航结构",
        "## 状态栏与胶囊",
        "## 返回兜底",
        "## 页面 offset",
        "## 页面接入 checklist",
        "## 截图验收矩阵",
        "## DevTools 与真机边界",
        "## 安全边界",
        "## 引用示例",
    ]:
        assert heading in source


def test_miniapp_custom_navigation_best_practice_covers_matrix_and_evidence_boundaries() -> None:
    source = _read_best_practice()

    for term in [
        "首页、搜索、分类、商品列表、商品详情、收藏、证书、门店信息",
        "320 pt、375 pt、430 pt",
        "iPhone 刘海屏",
        "iPhone 非刘海屏",
        "Android 常见机型",
        "DevTools evidence 不等同于真机验收",
        "没有真机记录时不得写作真机通过",
        "blocked",
        "not_applicable",
        "follow_up",
    ]:
        assert term in source


def test_miniapp_custom_navigation_best_practice_covers_security_and_references() -> None:
    source = _read_best_practice()
    readme = README.read_text(encoding="utf-8")

    for reference in [
        "REQ-0053-miniapp-custom-navigation-best-practice",
        "openspec/changes/add-miniapp-custom-navigation-best-practice/",
        "REQ-0048-miniapp-global-custom-navigation-bar",
        "REQ-0052-miniapp-device-evidence-template",
        "docs/standards/miniapp-device-evidence-template.md",
        "docs/knowledge-base/retrospectives/sprint-008-retrospective.md",
    ]:
        assert reference in source

    for forbidden_boundary in [
        "本机绝对路径",
        "Authorization header",
        ".env",
        "真实密钥",
        "MinIO 凭据",
        "真实客户数据",
    ]:
        assert forbidden_boundary in source

    assert "best-practices/miniapp-custom-navigation.md" in readme
    assert not re.search(r"/Users/[^`\\s]+", source)
