---
change_id: add-admin-list-page-contract
type: add
status: proposed
created_at: 2026-07-10 20:40:55
updated_at: 2026-07-10 20:40:55
source_requirement: REQ-0028-admin-list-page-contract
iteration: sprint-005
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
requires_orval: false
requires_docker_compose_validation: false
ui_strategy: design-system-composition
prototype_priority:
  - issues/requirements/archive/REQ-0028-admin-list-page-contract/prototype/web/admin-list-page-contract.html
  - issues/requirements/archive/REQ-0028-admin-list-page-contract/prototype/web/admin-list-page-contract-context.md
  - issues/requirements/archive/REQ-0028-admin-list-page-contract/acceptance.md
  - rules/ui-design.md
  - openspec/specs/web-client/spec.md
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
cross_cutting_tags:
  - admin-list
png_checklist:
  required: false
  reason: REQ-0028 标记 Partially Ready，PNG Golden Reference 待人工或实现阶段导出；HTML prototype 与 context 已足以进入 req-opsx。
---

# OpenSpec Change Trace

## 来源

- REQ：`issues/requirements/archive/REQ-0028-admin-list-page-contract/`
- Sprint：`iterations/change/sprint-005/`
- 关联 BUG：`BUG-0055-admin-list-layout-unification`

## 冲突处理

- HTML prototype 是结构最高优先级，只作为 Design System 样例和模板结构参考。
- 实现不得直接复制 prototype 裸 Hex；必须使用 semantic token、`cn()` 和现有管理端样式基线。
- `REQ-0029-admin-list-foundation-components` 负责基础组件和分页窗口工具；本 Change 负责页面级模板组合和复用门禁。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-10 20:40:55 | /req-opsx | 从 REQ-0028 创建 OpenSpec Change `add-admin-list-page-contract`。 |
