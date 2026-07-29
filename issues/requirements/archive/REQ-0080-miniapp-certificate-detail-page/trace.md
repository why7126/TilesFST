---
requirement_id: REQ-0080-miniapp-certificate-detail-page
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-29 07:57:17
updated_at: 2026-07-29 09:28:01
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0080-miniapp-certificate-detail-page
requirement_name: miniapp-certificate-detail-page
requirement_type: 小程序 / 品牌证书 / 详情页
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期
related_requirements:
  - REQ-0038-brand-certificate-management
  - REQ-0057-certificate-list-page
  - REQ-0078-certificate-multiple-images-main-image
  - REQ-0044-miniapp-sku-detail-page
related_changes:
  - add-miniapp-certificate-detail-page
lifecycle:
  captured: 2026-07-29 07:57:17
  generated: 2026-07-29 08:03:37
  completed: 2026-07-29 08:06:38
  reviewed: 2026-07-29 08:15:17
  approved: 2026-07-29 08:15:17
iteration: sprint-013
openspec_changes:
  - change_id: add-miniapp-certificate-detail-page
    type: add
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐，并提供小程序 prototype 策略；管理端横切 AC 判定为 N/A，小程序导航专项已写入验收。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/prototype-context.md
  - prototype/miniapp/certificate-detail.html
expected_openspec_change: add-miniapp-certificate-detail-page
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-012-retrospective.md
cross_cutting_tags: []
knowledge_base_summary: 本 REQ 为小程序公开端详情页，未命中 admin-list/admin-form/admin-modal/media-upload 管理端横切标签；验收已引用 miniapp-custom-navigation，覆盖分享直达、返回兜底、胶囊 reserve、页面 offset 与 DevTools/真机 evidence 边界。Sprint-012 复盘提醒跨端和媒体类需求需写清 API/DB/安全/测试边界，已在 acceptance.md 的 API、数据、安全和非功能 AC 中体现。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-29 09:22:16 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-certificate-detail-page） |
| 2026-07-29 09:21:55 | /opsx-archive | Change `add-miniapp-certificate-detail-page` 已归档，状态同步完成。 |
| 2026-07-29 08:51:04 | /opsx-apply | Change `add-miniapp-certificate-detail-page` apply 完成，待 archive。 |
| 2026-07-29 08:50:49 | /opsx-apply | Change `add-miniapp-certificate-detail-page` apply 进行中，待补齐剩余验收。 |
| 2026-07-29 08:24:32 | `/sprint-propose` | 纳入 `sprint-013` 正式范围，关联 Change `add-miniapp-certificate-detail-page`。 |
| 2026-07-29 08:19:01 | `/req-opsx` | 创建 OpenSpec Change `add-miniapp-certificate-detail-page`，状态 proposed。 |
| 2026-07-29 08:15:53 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-29 08:15:17 | `/req-review --approve` | 需求评审通过，允许进入 /req-opsx 与 Sprint 规划。 |
| 2026-07-29 08:06:38 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/miniapp；管理端横切 AC 判定为 N/A，补充小程序导航专项验收，状态更新为 pending_review。 |
| 2026-07-29 08:03:37 | `/req-generate` | 生成 requirement.md，状态更新为 draft。 |
| 2026-07-29 07:57:17 | `/capture` | 记录微信小程序新增证书详情页需求，设计参照商品详情页。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-29 09:21:55 workflow-sync：状态同步为 done（Change archived）
