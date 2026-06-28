---
requirement_id: REQ-0012-object-storage-key-layout
status: done
lifecycle_stage: archive
priority: P1
iteration: sprint-003
created_at: 2026-06-27 22:15:10
updated_at: 2026-06-28 19:40:42
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0012-object-storage-key-layout
requirement_name: object-storage-key-layout
requirement_type: 基础设施 / 对象存储
priority: P1
status: done
iteration: sprint-003
owner: product
source: 技术优化
target_clients:
  web_admin: 间接（上传 URL）
  web_catalog: 间接（媒体展示）
  wechat_miniapp: 不涉及
related_requirements:
  - REQ-0006-tile-sku-management
  - REQ-0005-brand-management
  - REQ-0005-user-management
suggested_change: update-object-storage-key-layout
migration_strategy: scheme_a_one_shot_script
lifecycle:
  captured: 2026-06-27 22:15:10
  generated: 2026-06-27 22:15:10
  completed: 2026-06-27 22:17:37
  reviewed: 2026-06-27 22:20:13
  approved: 2026-06-27 22:20:13
openspec_changes:
  - change_id: update-object-storage-key-layout
    type: update
    status: archived
documents:
  capture: issues/requirements/archive/REQ-0012-object-storage-key-layout/capture.md
  requirement: issues/requirements/archive/REQ-0012-object-storage-key-layout/requirement.md
  user_stories: issues/requirements/archive/REQ-0012-object-storage-key-layout/user-stories.md
  business_flow: issues/requirements/archive/REQ-0012-object-storage-key-layout/business-flow.md
  acceptance: issues/requirements/archive/REQ-0012-object-storage-key-layout/acceptance.md
  prototype: N/A（基础设施，无 UI 原型）```

## Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| requirement.md | done |
| user-stories.md | done |
| business-flow.md | done |
| acceptance.md | done |
| review.md | done |
| prototype | N/A |

**Readiness:** Ready（已评审 approved）

## 关键决策（req-complete 敲定）

| 项 | 决策 |
|---|---|
| 迁移策略 | **方案 A**：一次性迁移脚本（dry-run + apply），非长期双读 |
| 迁移脚本 | `scripts/migrate_object_keys.py`（OpenSpec apply 阶段实现） |
| UI 原型 | 不需要 |
| 建议 Change | `update-object-storage-key-layout` |

## 变更记录

| 2026-06-28 19:23:07 | lifecycle-stage-migrate | review → archive（backfill opsx-archive hook (sprint-003)） |
| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 12:30:00 | `migrate_object_keys.py --apply` | 8 条 legacy key 迁移完成；dry-run 复检 0 条；品牌 Logo 冒烟 4/4 200 |
| 2026-06-28 11:57:55 | `/opsx-archive` | change archived；openspec_changes → archived |
| 2026-06-28 12:00:00 | `/sprint-apply` | update-object-storage-key-layout apply 完成 |
| 2026-06-28 10:32:00 | `/req-opsx` | 创建 change update-object-storage-key-layout |
| 2026-06-28 10:27:18 | `/sprint-propose` | 纳入 sprint-003；status → in_sprint |
| 2026-06-27 22:33:15 | lifecycle-stage-migrate | 迁入 `review/`（status → stage 映射） |
| 2026-06-27 22:15:10 | `/req-capture`（随 generate 落盘） | 记录对象 Key 前缀与形态优化 |
| 2026-06-27 22:15:10 | `/req-generate` | 生成 requirement.md；status → draft |
| 2026-06-27 22:17:37 | `/req-complete` | 补齐 user-stories、business-flow、acceptance；Readiness → Ready |
| 2026-06-27 22:20:13 | `/req-review --approve` | REV-REQ-0012-001 评审通过 |
