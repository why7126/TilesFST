---
change_id: add-miniapp-custom-navigation-best-practice
type: add
status: proposed
created_at: 2026-07-19 19:43:26
updated_at: 2026-07-19 19:43:26
source_requirement: REQ-0053-miniapp-custom-navigation-best-practice
iteration: sprint-009
related_requirements:
  - REQ-0048-miniapp-global-custom-navigation-bar
  - REQ-0052-miniapp-device-evidence-template
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
target_capabilities:
  - miniapp-global-custom-navigation-bar
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
---

# Trace

```yaml
change_id: add-miniapp-custom-navigation-best-practice
status: proposed
source_requirement: REQ-0053-miniapp-custom-navigation-best-practice
iteration: sprint-009
openspec_capability: miniapp-global-custom-navigation-bar
expected_output:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/README.md
non_goals:
  - src/miniapp runtime changes
  - API changes
  - DB changes
  - Orval generation
  - Docker Compose changes
```

## 来源

| 类型 | 路径 |
|---|---|
| REQ trace | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/acceptance.md` |
| Prototype | `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/prototype/miniapp/` |
| Knowledge base | `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` |
| Best practice | `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` |

## Conflict Resolution

REQ-0053 的 prototype 仅作为 best-practice 信息架构原型，不是小程序页面视觉稿；本 Change 不要求把 prototype 转为 WXML/WXSS。验收以 `acceptance.md` 和 delta spec 中可测试条款为准。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 20:59:58 | `openspec validate add-miniapp-custom-navigation-best-practice --strict` | 通过：Change valid |
| 2026-07-19 20:59:58 | `uv run pytest tests/test_miniapp_custom_navigation_best_practice.py tests/test_miniapp_device_evidence_template.py` | 通过：6 passed |
| 2026-07-19 20:06:00 | /opsx-apply | 新增小程序自定义导航 best-practice 文档、知识库索引与轻量校验 |
| 2026-07-19 19:43:26 | /req-opsx | 创建 OpenSpec Change，状态 proposed |
