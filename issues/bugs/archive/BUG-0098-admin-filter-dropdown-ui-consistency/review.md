---
bug_id: BUG-0098-admin-filter-dropdown-ui-consistency
title: 管理端筛选条件下拉框位置和 UI 样式不统一
status: done
severity: medium
review_result: approved
reviewed_at: 2026-07-31 21:44:05
reviewer: AI
created_at: 2026-07-31 21:44:05
updated_at: 2026-07-31 22:59:41
---

# BUG Review

## 评审结论

批准修复。

管理端多个页面已经存在筛选下拉能力，但下拉框位置、弹层对齐、状态表现和 UI 样式未与瓷砖类目页保持一致，属于既有管理端筛选体验的一致性缺陷。该问题横跨多个后台页面，会影响高频筛选操作的可预期性和视觉专业度，建议进入 OpenSpec 修复流程。

## 评审清单

- [x] 可复现或根因充分：可通过对比瓷砖类目页与其他管理端页面的筛选下拉框复现；根因初判为筛选控件缺少统一复用约束或验收基准。
- [x] 严重等级合理：`medium`，不阻断数据维护，但影响多页面高频后台筛选体验。
- [x] 回归验收明确：acceptance.md 已覆盖下拉位置、弹层对齐、选项状态、重置表现、接口语义不变、Design System 约束和基础可用性。
- [x] 是否需 hotfix 路径：不需要 hotfix，可按常规 BUG 修复进入 `/bug-opsx` 与 Sprint 规划。

## 处理建议

- 后续通过 `/bug-opsx BUG-0098-admin-filter-dropdown-ui-consistency` 创建 OpenSpec Change。
- 修复设计应优先复用或抽象管理端统一筛选下拉组件，避免逐页局部样式补丁。
- 修复验收需重点确认不改变现有筛选参数、接口请求和查询结果语义。
