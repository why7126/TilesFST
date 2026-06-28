---
created_at: 2026-06-28 12:37:33
title: 缺陷追踪
purpose: BUG-0022 个人资料基础资料区角色/状态信息重复
content: 记录个人资料页基础资料与账号安全卡片信息冗余
owner: product
status: done
lifecycle_stage: archive
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0022-profile-basic-info-redundant-role-status
bug_name: profile-basic-info-redundant-role-status
severity: low
status: done
iteration: sprint-003
related_requirement: REQ-0014-profile-page
related_bug: BUG-0023-profile-duplicate-save-buttons
related_change: fix-profile-basic-info-redundant-role-status
suggested_fix_change: fix-profile-basic-info-redundant-role-status
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 12:37:33
  generated: 2026-06-28 12:52:53
  completed: 2026-06-28 12:54:36
  reviewed: 2026-06-28 12:56:26
  approved: 2026-06-28 12:56:26
openspec_changes:
  - change_id: fix-profile-basic-info-redundant-role-status
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

**Readiness:** Ready — REV-BUG-0022-001 approved；可 bug-opsx

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0014 交付后 UX polish） |
| 根因类型 | design / frontend-ui（双区重复展示） |
| 修复面 | ProfilePage.tsx + REQ-0014 / prototype / OpenSpec delta |
| UX 定稿 | 角色/状态仅在账号安全卡片；AC-011 MODIFIED |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| bug | `bug.md` |
| root-cause | `root-cause.md` |
| workaround | `workaround.md` |
| acceptance | `acceptance.md` |
| 父需求 | `issues/requirements/archive/REQ-0014-profile-page/` |
| 关联 BUG | `issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/` |
| 组件 | `src/web/src/pages/admin/ProfilePage.tsx` |

## 5. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 12:58:03 | `/bug-opsx` | 创建 fix-profile-basic-info-redundant-role-status；status proposed |
| 2026-06-28 12:56:26 | `/bug-review --approve` | REV-BUG-0022-001 评审通过；plan → review |
| 2026-06-28 12:54:36 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；Readiness → Ready |
| 2026-06-28 12:52:53 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 12:45:00 | UX 定稿 | BUG-0022 采纳；移除表单内角色/状态；AC-011 MODIFIED |
| 2026-06-28 12:37:33 | `/bug-capture` | 记录基础资料区所属角色/账号状态与账号安全卡片重复 |
