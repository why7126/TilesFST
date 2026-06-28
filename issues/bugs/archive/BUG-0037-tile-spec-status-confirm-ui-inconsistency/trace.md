---
created_at: 2026-06-28 16:06:42
title: 缺陷追踪
purpose: BUG-0037 瓷砖规格页启用/停用/删除确认弹窗与类目页 UI/UE 不一致
content: 记录确认 Dialog 结构、文案与按钮差异
owner: product
status: done
lifecycle_stage: archive
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0037-tile-spec-status-confirm-ui-inconsistency
bug_name: tile-spec-status-confirm-ui-inconsistency
severity: medium
status: done
related_requirement: REQ-0009-tile-spec-management
related_bug:
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:06:42
  draft: 2026-06-28 16:12:27
  enriching: 2026-06-28 16:14:20
  pending_review: 2026-06-28 16:14:20
  approved: 2026-06-28 16:16:41
suggested_fix_change: fix-tile-spec-status-confirm-ui
openspec_changes:
  - change_id: fix-tile-spec-status-confirm-ui
    type: fix
    status: archived```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Approved — 可 `/bug-opsx`

## 3. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 16:06:42 | `/bug-capture` | 记录规格页启用/停用/删除确认弹窗与类目页 UI/UE 不一致 |
| 2026-06-28 16:12:27 | `/bug-generate` | 生成 bug.md；trace → draft |
| 2026-06-28 16:14:20 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；trace → pending_review |
| 2026-06-28 16:16:41 | `/bug-review --approve` | 评审通过；status → approved |
| 2026-06-28 16:18:39 | `/bug-opsx` | 创建 OpenSpec change `fix-tile-spec-status-confirm-ui` |
| 2026-06-28 16:35:12 | `/opsx-apply` | 启停/删除 confirm 对齐类目页；vitest 3/3 pass |
| 2026-06-28 16:48:07 | `/opsx-archive` | change archived；spec 合并至 `web-client`；BUG → done |
| 2026-06-28 16:52:00 | Docker 冒烟 | `smoke-tile-spec-docker.sh` + BUG-0037 bundle/API 检查通过 |
