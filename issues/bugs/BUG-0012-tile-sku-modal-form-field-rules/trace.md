---
created_at: 2026-06-27 08:56:54
title: 缺陷追踪
purpose: BUG-0012 SKU弹窗表面工艺/参考价格字段规则调整
content: 记录表面工艺改非必填、参考价格改必填且默认0的产品规则偏差
owner: product
status: done
note: /bug-review 已批准；可 /bug-opsx
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0012-tile-sku-modal-form-field-rules
bug_name: tile-sku-modal-form-field-rules
severity: medium
status: done
iteration: sprint-002
related_requirement: REQ-0006-tile-sku-management
related_change: fix-tile-sku-modal-form-field-rules
suggested_fix_change: fix-tile-sku-modal-form-field-rules
target_clients:
  web_admin: 是
  backend: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 08:56:54
  generated: 2026-06-27 11:33:47
  completed: 2026-06-27 11:35:29
  reviewed: 2026-06-27 11:43:36
  approved: 2026-06-27 11:43:36
  in_sprint: 2026-06-27 11:45:13
  opsx_created: 2026-06-27 11:47:09
  applied: 2026-06-27 11:50:30
openspec_changes:
  - change_id: fix-tile-sku-modal-form-field-rules
    type: fix
    status: archived
    bug_id: BUG-0012-tile-sku-modal-form-field-rules```

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
| 需求 vs 缺陷 | 缺陷（实现/规则与产品验收预期不符；fix 时须 REQ acceptance delta） |
| 根因类型 | product-rule / validation |
| 修复面 | SKU 弹窗表单、API 校验、publish 策略、REQ-0006 acceptance |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| bug | `bug.md` |
| root-cause | `root-cause.md` |
| workaround | `workaround.md` |
| acceptance | `acceptance.md` |
| 父需求 | `issues/requirements/REQ-0006-tile-sku-management/` |
| 建议 fix change | `fix-tile-sku-modal-form-field-rules` |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 08:56:54 | `/bug-capture` | 记录表面工艺非必填、参考价格必填默认0的表单规则调整 |
| 2026-06-27 11:33:47 | `/bug-generate` | 生成 bug.md；trace → draft |
| 2026-06-27 11:35:29 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；trace → pending_review |
| 2026-06-27 11:43:36 | `/bug-review --approve` | 评审通过；status → approved |
| 2026-06-27 11:45:13 | `/sprint-propose` | 纳入 sprint-002 正式范围 |
| 2026-06-27 11:47:09 | `/bug-opsx` | 创建 `fix-tile-sku-modal-form-field-rules` |
| 2026-06-27 11:50:30 | `/opsx-apply` | 实现字段规则修复；20/21 tasks |

## 6. 后续动作

- `/opsx-archive fix-tile-sku-modal-form-field-rules`
