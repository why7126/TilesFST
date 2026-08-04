---
change_id: update-miniapp-network-panel-release-checklist
status: archived
type: update
created_at: 2026-08-04 08:50:00
updated_at: 2026-08-04 09:34:00
source_requirement: REQ-0096-miniapp-network-panel-release-checklist
source_requirement_path: issues/requirements/archive/REQ-0096-miniapp-network-panel-release-checklist
iteration: sprint-019
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-device-evidence-template
    - product-release-management
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-014-retrospective.md
  - docs/standards/miniapp-device-evidence-template.md
  - rules/media.md
  - rules/object-storage.md
---

# Change Trace

## 来源

- REQ：`REQ-0096-miniapp-network-panel-release-checklist`
- 状态：approved
- 目标：将小程序 DevTools/体验版 Network evidence 纳入 release/miniapp 发布准备清单。

## 影响分析

| 领域 | 影响 | 说明 |
|---|---|---|
| backend | 否 | 不新增或修改后端 API。 |
| web | 否 | 不修改 Web 管理端或店主 Web。 |
| miniapp | 是 | 修改小程序发布准备命令、脚本 checklist 和 README，不改业务页面。 |
| admin | 否 | 不影响管理端权限或页面。 |
| database | 否 | 不涉及表结构或迁移。 |
| storage | 否 | 不改对象存储策略，仅要求发布前记录资源加载结论。 |
| api | 否 | 不改 OpenAPI 或 Orval。 |

## Readiness

| 项 | 状态 | 说明 |
|---|---|---|
| proposal.md | ready | 已定义背景、变更内容、能力范围和影响。 |
| design.md | ready | 已定义复用 evidence 模板、人工 checklist 和确认记录策略。 |
| specs | ready | 已为两个现有 capability 编写 ADDED delta requirements。 |
| tasks.md | ready | 已拆分标准、脚本、测试和验证任务。 |

## 实施记录

| 项 | 结论 |
|---|---|
| 标准文档 | 已更新 `docs/standards/miniapp-device-evidence-template.md`，新增 `network_devtools`、`network_trial` 来源、字段、安全边界、YAML 示例和表格示例。 |
| Skill | 已更新 `.agents/skills/miniapp-prepare/SKILL.md` 与 `.agents/skills/miniapp-confirm/SKILL.md`，区分自动门禁与人工 Network checklist，并承接 DevTools Network、体验版 Network、阻塞项和剩余风险。 |
| 小程序 README | 已更新 `src/miniapp/README.md`，补充 release/miniapp 准备中的 Network evidence 边界。 |
| 脚本 | 已更新 `scripts/miniapp-env.py` 的 `checklist()` 与 confirm 安全摘要，Network evidence 为待人工执行项，不自动标记通过。 |
| 测试 | 已补充 `tests/test_miniapp_static.py::test_miniapp_prepare_network_checklist_is_manual_evidence`，并运行 `uv run pytest tests/test_miniapp_static.py` 通过。 |
| API / DB / Orval / Docker | 不影响 API、数据库、OpenAPI/Orval、Docker Compose、对象存储策略、Web 管理端、店主 Web 或小程序业务页面。 |

## 后续门禁

来源于 REQ 的 Change 已纳入 `sprint-019`，完成 `/opsx-apply`，并归档至 `openspec/archive/2026-08-04-update-miniapp-network-panel-release-checklist/`。
