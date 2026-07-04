---
title: 产品版本发布与公告管理 Trace
purpose: 记录 REQ-0026 产品版本发布与公告管理的生命周期、状态与后续 OpenSpec 关联
created_at: 2026-07-02 13:04:17
updated_at: 2026-07-04 08:16:02
owner: product
status: done
---

requirement_id: REQ-0026-product-release-management
status: done
priority: P1
created_at: 2026-07-02 13:04:17
updated_at: 2026-07-03 23:56:30
lifecycle_stage: archive
lifecycle:
  captured: 2026-07-02 13:04:17
  generated: 2026-07-02 13:16:07
  completed: 2026-07-02 13:39:28
  reviewed: 2026-07-02 13:56:11
  approved: 2026-07-02 13:56:11
  archived: 2026-07-03 23:56:30
iteration: sprint-004
openspec_changes:
  - change_id: add-product-release-management
    type: add
    status: archived
related_requirements:
  - REQ-0010-product-version-display
knowledge_base_refs: []
cross_cutting_tags: []
retrospective_refs:
  - docs/knowledge-base/retrospectives/sprint-003-retrospective.md

# Trace

## 当前状态

| 字段 | 内容 |
|---|---|
| 需求 | REQ-0026-product-release-management |
| 状态 | done |
| 阶段目录 | archive |
| 优先级 | P1 |
| 父/关联需求 | REQ-0010-product-version-display |
| 关联迭代 | sprint-004 |
| 关联 OpenSpec Change | add-product-release-management |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-02 13:04:17 | /req-capture | 记录产品版本发布与公告管理需求 |
| 2026-07-02 13:11:29 | /req-capture | 补充产品发布合并 Sprint、公开 Mintlify 公告、releases 目录、发布校验与公告内容约束 |
| 2026-07-02 13:16:07 | /req-generate | 生成 requirement.md，状态推进为 draft |
| 2026-07-02 13:39:28 | /req-complete | 补齐 user-stories、business-flow、acceptance；无 UI 横切标签，knowledge-base gate 为 N/A；参考 sprint-003 复盘中的发布/验收门禁风险 |
| 2026-07-02 13:56:11 | /req-review --approve | 评审通过，准备从 plan 迁入 review |
| 2026-07-02 13:57:13 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-02 14:44:48 | /sprint-propose REQ-0026 纳入 sprint-004 | 已评审需求纳入 sprint-004，OpenSpec Change 待 `/req-opsx` |
| 2026-07-02 14:55:51 | /req-opsx REQ-0026 | 创建 OpenSpec Change `add-product-release-management` |
| 2026-07-02 15:27:36 | /opsx-apply add-product-release-management | 完成发布目录治理、模板、校验脚本、release 命令族、测试与同步 |
| 2026-07-03 23:56:30 | /opsx-archive add-product-release-management | Change 已归档，状态同步为 done，准备迁入 archive |
| 2026-07-03 23:56:52 | lifecycle-stage-migrate | review → archive（/opsx-archive add-product-release-management） |
