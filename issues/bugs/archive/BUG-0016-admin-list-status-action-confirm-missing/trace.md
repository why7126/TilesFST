---
created_at: 2026-06-27 12:03:34
title: 缺陷追踪
purpose: BUG-0016 用户/SKU 列表状态操作缺少二次确认
content: 记录冻结上下架等操作未弹 DS confirm modal
owner: product
status: done
lifecycle_stage: archive
note: 经 /opsx-archive 归档 fix-admin-list-status-action-confirm
iteration: sprint-002
readiness: approved
updated_at: 2026-06-27 22:33:15
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0016-admin-list-status-action-confirm-missing
bug_name: admin-list-status-action-confirm-missing
severity: medium
status: done
iteration: sprint-002
related_requirement: REQ-0008-brand-status-confirm
related_change: fix-admin-list-status-action-confirm
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 12:03:34
  draft: 2026-06-27 13:05:16
  enriching: 2026-06-27 13:12:51
  pending_review: 2026-06-27 13:12:51
  approved: 2026-06-27 13:15:21
openspec_changes:
  - change_id: fix-admin-list-status-action-confirm
    type: fix
    status: archived
    requirement_id: REQ-0008-brand-status-confirm
    iteration: sprint-002```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done（品牌范围过时，以 bug.md 为准） |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Approved（可 `/bug-opsx`、可纳入 Sprint）

## 3. 修复范围摘要

| 页面 | 须补 confirm | 已满足 / 排除 |
|---|---|---|
| 用户管理 | 冻结、解冻、删除（modal 化） | 重置密码 → BUG-0017 |
| 瓷砖 SKU | 上架、下架、恢复 | 删除已有 modal |
| 瓷砖品牌 | — | REQ-0008 已交付 |
| 瓷砖类目 | — | REQ-0007 参考实现 |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| Golden Reference | `TileCategoryManagementPage.tsx`、`BrandManagementPage.tsx` |
| 启停 context | `REQ-0008/.../brand-status-confirm-context.md` |
| 建议 change | `fix-admin-list-status-action-confirm`（**archived**） |
| OpenSpec | `openspec/changes/archive/2026-06-27-fix-admin-list-status-action-confirm/` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 12:03:34 | `/capture` | 记录品牌/用户列表状态变更缺少二次确认 |
| 2026-06-27 13:05:16 | `/bug-generate` | 生成 bug.md；收窄范围（品牌已修复；聚焦用户冻结/SKU 上下架） |
| 2026-06-27 13:12:51 | `/bug-complete` | 补齐 root-cause、workaround、acceptance |
| 2026-06-27 13:15:21 | `/bug-review --approve` | 评审通过 |
| 2026-06-27 13:17:34 | `/sprint-propose` | 纳入 sprint-002 正式规划 |
| 2026-06-27 13:18:35 | `/bug-opsx` | 创建 `fix-admin-list-status-action-confirm`（proposed） |
| 2026-06-27 13:23:11 | `/opsx-apply` | 用户/SKU DS confirm modal + Vitest + build（applied） |
| 2026-06-27 13:27:11 | `/opsx-archive` | archived；`web-client` spec +2 requirements |

## 6. 后续动作

- （可选）Docker 手工冒烟 `/admin/users`、`/admin/tile-skus` confirm 流程
