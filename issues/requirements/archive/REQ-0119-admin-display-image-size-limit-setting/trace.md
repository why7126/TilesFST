---
requirement_id: REQ-0119-admin-display-image-size-limit-setting
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-22 21:12:30
updated_at: 2026-08-22 22:28:42
openspec_changes:
  - change_id: add-admin-display-image-size-limit-setting
    type: update
    status: archived
related_changes:
  - add-admin-display-image-size-limit-setting
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0119-admin-display-image-size-limit-setting
requirement_name: admin-display-image-size-limit-setting
requirement_type: 媒体治理 / 系统设置
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 间接受益
  wechat_miniapp: 间接受益
related_requirements:
  - REQ-0115-media-multi-variant-images
  - REQ-0099-global-thumbnail-size-limit
related_changes:
  - add-admin-display-image-size-limit-setting
lifecycle:
  captured: 2026-08-22 21:12:30
  generated: 2026-08-22 21:16:01
  completed: 2026-08-22 21:19:48
  reviewed: 2026-08-22 21:29:55
  approved: 2026-08-22 21:29:55
  scoped: 2026-08-22 21:38:35
iteration: sprint-025
openspec_changes:
  - change_id: add-admin-display-image-size-limit-setting
    type: update
    status: archived
readiness: Partially Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 prototype 策略；命中的 knowledge-base best-practices 当前为 draft，PNG 待后续 OpenSpec Change 阶段导出。
cross_cutting_tags:
  - media-upload
  - object-storage
  - system-settings
  - admin-web
  - admin-form
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-form-page-consistency.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
  - prototype/web/system-settings-media-display-size.html
expected_openspec_change: add-admin-display-image-size-limit-setting
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 22:20:00 | lifecycle-stage-migrate | review → archive（/opsx-archive add-admin-display-image-size-limit-setting） |
| 2026-08-22 22:19:53 | /opsx-archive | Change `add-admin-display-image-size-limit-setting` 已归档，状态同步完成。 |
| 2026-08-22 22:15:47 | /opsx-modify | Change `add-admin-display-image-size-limit-setting` 验收返修已同步，待复验或 archive。 |
| 2026-08-22 22:05:20 | /opsx-apply | Change `add-admin-display-image-size-limit-setting` apply 完成，待 archive。 |
| 2026-08-22 22:07:00 | `/opsx-apply REQ-0119` | 完成实现与验证；`display_max_size_kb` 默认 768KB，已接入系统设置、上传、SKU 正式化、维护任务、管理端 UI、OpenAPI/Orval 和文档 |
| 2026-08-22 21:45:57 | `/req-opsx REQ-0119` | 创建 `add-admin-display-image-size-limit-setting` 并回填 sprint-025；下一步 `/opsx-apply REQ-0119` |
| 2026-08-22 21:38:35 | `/sprint-propose --req REQ-0119` | 已纳入 sprint-025；估算 M / 3 SP / 3 人天，下一步创建 OpenSpec Change |
| 2026-08-22 21:30:36 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-22 21:29:55 | `/req-review` | 评审通过；建议先纳入 Sprint，再创建 OpenSpec Change |
| 2026-08-22 21:19:48 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype 策略；写入 admin-form、media-upload 横切 AC，并引用 sprint-024 媒体 URL 语义复盘 |
| 2026-08-22 21:16:01 | `/req-generate` | 生成 PRD，确认新增 display 图体积目标配置、默认值 768KB、与缩略图配置独立且不自动重建历史对象 |
| 2026-08-22 21:12:30 | `/req-capture` | 记录管理端媒体与存储新增 display 图体积目标上限配置需求，默认值沿用 768KB |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-22 22:19:53 workflow-sync：状态同步为 done（Change archived）
