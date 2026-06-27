---
created_at: 2026-06-27 10:54:19
title: 缺陷追踪
purpose: BUG-0013 产品版本号 UI 与原型及 Design System 不一致
content: 记录管理端侧边栏 brand-head 版本 pill 视觉未对齐 REQ-0010 原型
owner: product
status: done
note: /bug-review 评审通过；可 bug-opsx
iteration: null
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0013-product-version-ui-inconsistency
bug_name: product-version-ui-inconsistency
severity: medium
status: done
iteration: null
related_requirement: REQ-0010-product-version-display
related_change: add-product-version-display
suggested_fix_change: fix-product-version-ui-inconsistency
target_clients:
  web_admin: 是
  web_catalog: 是（共用 ProductVersionBadge）
environment: local|docker
lifecycle:
  captured: 2026-06-27 10:54:19
  generated: 2026-06-27 10:57:13
  completed: 2026-06-27 10:59:01
  reviewed: 2026-06-27 11:00:42
  approved: 2026-06-27 11:00:42
  opsx_created: 2026-06-27 11:03:01
  applied: 2026-06-27 11:08:57
openspec_changes:
  - change_id: fix-product-version-ui-inconsistency
    type: fix
    status: proposed
    bug_id: BUG-0013-product-version-ui-inconsistency```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0010 已实现但视觉验收未达标） |
| 根因类型 | design / frontend-ui（ProductVersionBadge 未对齐 DS Badge 与原型 pill） |
| 修复面 | Web 管理端 + 店主端 brand-head / ProductVersionBadge（或 Badge variant） |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| bug | `bug.md` |
| root-cause | `root-cause.md` |
| workaround | `workaround.md` |
| acceptance | `acceptance.md` |
| 父需求 | `issues/requirements/REQ-0010-product-version-display/` |
| UI 规范 | `rules/ui-design.md` §8 |
| 管理端原型 | `issues/requirements/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html` |
| Golden Reference | `issues/requirements/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png` |
| 实际截图 | `screenshots/admin-sidebar-version-actual.png` |
| 实现组件 | `src/web/src/shared/ui/product-version-badge.tsx` |
| DS Badge 参考 | `src/web/src/shared/ui/badge.tsx` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 10:54:19 | `/bug-capture` | 记录产品版本号 UI 与原型及 Design System 不一致 |
| 2026-06-27 10:57:13 | `/bug-generate` | 生成 bug.md |
| 2026-06-27 10:59:01 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；Readiness → Ready |
| 2026-06-27 11:00:42 | `/bug-review --approve` | 评审通过，状态 → approved |
| 2026-06-27 11:03:01 | `/bug-opsx` | 创建 `fix-product-version-ui-inconsistency` |
| 2026-06-27 11:08:57 | `/opsx-apply fix-product-version-ui-inconsistency` | Badge version variant + admin CSS + Vitest |

## 6. 后续动作

- `/opsx-archive fix-product-version-ui-inconsistency`
