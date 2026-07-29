---
requirement_id: REQ-0081-release-image-build-governance
status: pending_review
priority: P1
created_at: 2026-07-29 10:00:08
updated_at: 2026-07-29 10:07:04
lifecycle:
  captured: 2026-07-29 10:00:08
  generated: 2026-07-29 10:04:35
  completed: 2026-07-29 10:07:04
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirements: []
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0081-release-image-build-governance
requirement_name: release-image-build-governance
requirement_type: 发布治理 / 镜像构建命令与门禁
priority: P1
status: pending_review
owner: product
source: 发布流程探索
target_clients:
  web_admin: 不直接影响
  web_catalog: 不直接影响
  wechat_miniapp: 不直接影响
related_requirements: []
related_changes: []
lifecycle:
  captured: 2026-07-29 10:00:08
  generated: 2026-07-29 10:04:35
  completed: 2026-07-29 10:07:04
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 trace；本 REQ 为发布/镜像构建命令治理，不涉及 UI prototype，knowledge-base UI 横切 AC 判定为 N/A。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
expected_openspec_change: null
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-013-retrospective.md
cross_cutting_tags: []
knowledge_base_summary: sprint-013 复盘提示 release-note/scope 增量同步、归档证据 fallback、发布边界 follow-up 管理仍需治理；本 REQ 将镜像计划、manifest 与 release gates 纳入发布流程，避免发布和交付证据脱节。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 10:07:04 | `/req-complete` | 补齐 user-stories、business-flow、acceptance；Knowledge-base gate 判定为 N/A（无 UI 横切标签），状态更新为 pending_review。 |
| 2026-07-29 10:04:35 | `/req-generate` | 生成 requirement.md，状态更新为 draft。 |
| 2026-07-29 10:00:08 | `/req-capture` | 记录发布镜像准备与构建治理需求，暂不创建 PRD 或 OpenSpec Change。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
