---
bug_id: BUG-0053-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表冗余系统接口信息且分页未与 SKU 页一致评审
severity: medium
status: approved
owner: product
review_result: approved
reviewed_at: 2026-07-01 14:02:42
created_at: 2026-07-01 14:02:42
updated_at: 2026-07-01 14:02:42
related_requirement: REQ-0022-admin-api-docs-menu
related_change: null
---

# 缺陷评审

## 评审结论

`approved`：确认修复。

该缺陷属于 REQ-0022 已交付页面的管理端列表一致性偏差，应进入后续 `/bug-opsx` 创建 `fix-api-docs-list-layout-pagination-inconsistent` 修复 Change。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `/admin/api-docs` 当前存在固定标题「系统接口」，且底部没有真实分页控件 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断访问，不影响权限安全，但影响列表一致性与操作体验 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖标题移除、分页交互、UI 一致性、权限与 Swagger 回归 |
| 是否需 hotfix 路径 | 不需要 | 影响范围集中在接口文档页，不涉及数据损坏、越权或核心链路阻断 |

## 产品确认

用户反馈中的「第一行【系统接口】信息」已确认为接口列表区标题。修复时 MUST 直接移除该标题，不改名保留，也不按接口数据行过滤处理。

## 后续动作

1. 执行 `/bug-opsx BUG-0053-api-docs-list-layout-pagination-inconsistent`。
2. 创建 `fix-api-docs-list-layout-pagination-inconsistent` OpenSpec Change。
3. 修复时优先在 Web 管理端完成前端分页与标题移除；除非实现方案改变 API 契约，否则不需要后端接口、数据库、MinIO 或 Orval 变更。
