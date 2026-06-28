---
created_at: 2026-06-27 08:42:28
title: 需求追踪
purpose: REQ-0008 品牌列表启停二次确认追踪
content: 关联父需求、参考实现与 OpenSpec
owner: product
status: done
lifecycle_stage: archive
note: fix-brand-status-confirm 已 archive（2026-06-26 21:24:30）
readiness: partially_ready
iteration: sprint-002
updated_at: 2026-06-27 22:33:15
---

# 需求追踪

## 1. 基本信息

```yaml
requirement_id: REQ-0008-brand-status-confirm
requirement_name: brand-status-confirm
requirement_type: 管理端 / UI 交互优化
priority: P1
status: done
iteration: sprint-002
parent_requirement: REQ-0005-brand-management
source: 产品反馈（品牌启停需二次确认）
target_users:
  - 后台管理员
  - 内部员工（employee）
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0005-brand-management
  - REQ-0007-tile-category-management-refine
related_changes:
  - add-brand-management
lifecycle:
  captured: 2026-06-26 20:51:18
  generated: 2026-06-26 20:56:55
  completed: 2026-06-26 20:58:31
  reviewed: 2026-06-26 21:08:08
  approved: 2026-06-26 21:08:08
openspec_changes:
  - change_id: fix-brand-status-confirm
    type: fix
    status: archived
    requirement_id: REQ-0008-brand-status-confirm
    iteration: sprint-002
    archived_at: 2026-06-26 21:24:30
    archive_path: openspec/changes/archive/2026-06-26-fix-brand-status-confirm```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | ✓ |
| requirement.md | ✓ |
| user-stories.md | ✓ |
| business-flow.md | ✓ |
| acceptance.md | ✓ |
| trace.md | ✓ |
| review.md | ✓ |
| prototype/web/brand-status-confirm-context.md | ✓ |
| prototype PNG | 待导出（非阻塞） |

**Readiness:** Partially Ready（缺 PNG golden reference，已交付）

## 3. 优化项摘要

| # | 项 | FR | 状态 |
|---|-----|-----|------|
| O-01 | 启停二次确认 | FR-001 ~ FR-002 | 已 archive |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| PRD | `requirement.md` |
| 用户故事 | `user-stories.md` |
| 业务流程 | `business-flow.md` |
| 验收 | `acceptance.md` |
| 评审 | `review.md` |
| 启停确认 context | `prototype/web/brand-status-confirm-context.md` |
| 父需求 | `issues/requirements/archive/REQ-0005-brand-management/` |
| 归档 Change | `openspec/changes/archive/2026-06-26-fix-brand-status-confirm/` |
| 实现 | `src/web/src/pages/admin/BrandManagementPage.tsx` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 20:51:18 | `/req-capture` | 记录品牌列表启停二次确认需求；parent=REQ-0005-brand-management |
| 2026-06-26 20:56:02 | 澄清确认 | 启停文案与删除/类目启停风格一致；停用正文补充「停用后前台将不再展示该品牌」 |
| 2026-06-26 20:56:55 | `/req-generate` | 生成 `requirement.md`；status → draft |
| 2026-06-26 20:58:31 | `/req-complete` | 补齐 user-stories / business-flow / acceptance / prototype context；status → pending_review |
| 2026-06-26 21:08:08 | `/req-review` | approved（REV-REQ-0008-001） |
| 2026-06-26 21:09:52 | Sprint scope update | 纳入 `sprint-002`；status → in_sprint |
| 2026-06-26 21:15:13 | `/req-opsx` | 创建 `fix-brand-status-confirm` |
| 2026-06-26 21:19:05 | `/opsx-apply` | 实现启停确认弹窗；vitest 5/5、build 通过 |
| 2026-06-26 21:24:30 | `/opsx-archive` | 归档至 `2026-06-26-fix-brand-status-confirm`；web-client spec 已同步 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0016-admin-list-status-action-confirm-missing | medium | done | fix-admin-list-status-action-confirm | 管理端用户/SKU 列表状态变更操作缺少二次确认弹窗 |
