---
requirement_id: REQ-0120-webp-derived-image-variants
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-22 21:32:10
updated_at: 2026-08-25 14:51:36
openspec_changes:
  - change_id: add-webp-derived-image-variants
    type: update
    status: archived
related_changes:
  - add-webp-derived-image-variants
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0120-webp-derived-image-variants
requirement_name: webp-derived-image-variants
requirement_type: 媒体治理 / 图片性能优化
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 本期
  web_catalog: 本期
  wechat_miniapp: 本期
related_requirements:
  - REQ-0115-media-multi-variant-images
related_changes:
  - add-webp-derived-image-variants
lifecycle:
  captured: 2026-08-22 21:32:10
  generated: 2026-08-22 21:37:49
  completed: 2026-08-22 21:45:57
  reviewed: 2026-08-22 21:51:08
  approved: 2026-08-22 21:51:08
iteration: sprint-025
openspec_changes:
  - change_id: add-webp-derived-image-variants
    type: update
    status: archived
readiness: Partially Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 prototype 策略；命中的 best-practices 当前为 draft，且本需求不新增独立 UI，HTML/PNG 原型暂不生成。
cross_cutting_tags:
  - media-upload
  - object-storage
  - image-variants
  - web-performance
  - miniapp-performance
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/knowledge-base/retrospectives/sprint-024-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/web/context.md
expected_openspec_change: add-webp-derived-image-variants
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 14:38:06 | lifecycle-stage-migrate | review → archive（/opsx-archive add-webp-derived-image-variants） |
| 2026-08-25 14:38:01 | /opsx-archive | Change `add-webp-derived-image-variants` 已归档，状态同步完成。 |
| 2026-08-25 14:19:17 | /opsx-modify | Change `add-webp-derived-image-variants` 验收返修已同步，待复验或 archive。 |
| 2026-08-25 14:18:06 | `/opsx-modify` | 补充 Docker Web `localhost:3000` SKU 图片上传与 `display.webp` 展示证据；上传接口、派生 URL、即时回显和资源收益均已记录，Docker Web 边界从待补更新为 pass。 |
| 2026-08-25 12:03:34 | evidence-update | 补充用户提供的小程序微信开发者工具截图证据：品牌页渲染可见，`.display.webp` 请求返回 `200 OK`，小程序四联 render 由 blocked 更新为 pass；Docker Web 上传边界仍待补。 |
| 2026-08-22 22:28:42 | /opsx-apply | Change `add-webp-derived-image-variants` apply 完成，待 archive。 |
| 2026-08-22 22:25:05 | `/opsx-apply` | 已实现 WebP 派生图策略并通过后端重点回归测试；验收状态为 `pending_manual_evidence`，待补 Docker Web 与小程序真实 Network/render evidence。 |
| 2026-08-22 22:01:19 | `/sprint-propose` | 纳入 sprint-025 正式范围；估算 M / 3 人天；待创建 OpenSpec Change |
| 2026-08-22 21:52:42 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-22 21:51:08 | `/req-review` | 评审通过；建议先纳入 Sprint，再创建 OpenSpec Change |
| 2026-08-22 21:45:57 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype 策略；写入 media-upload 和小程序媒体四联横切 AC，并引用 sprint-024 媒体 URL 语义复盘 |
| 2026-08-22 21:37:49 | `/req-generate` | 生成 PRD，确认原图保留上传格式、WebP 派生图策略、特殊格式跳过/暂不转码边界 |
| 2026-08-22 21:32:10 | `/req-capture` | 记录图片上传生成 WebP 展示图和缩略图需求，确认原图保留上传格式、端侧优先使用 WebP 派生图 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-08-25 14:38:01 workflow-sync：状态同步为 done（Change archived）
