---
requirement_id: REQ-0068-miniapp-sku-video-fullscreen-actions
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-23 23:11:09
updated_at: 2026-07-24 20:44:28
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags: []
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0068-miniapp-sku-video-fullscreen-actions
requirement_name: miniapp-sku-video-fullscreen-actions
requirement_type: 小程序 / 商品详情页视频全屏交互
priority: P1
status: done
lifecycle_stage: review
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期
related_requirements:
  - REQ-0044-miniapp-sku-detail-page
related_changes:
  - add-miniapp-sku-video-fullscreen-actions
lifecycle:
  captured: 2026-07-23 23:11:09
  generated: 2026-07-23 23:15:48
  completed: 2026-07-23 23:19:20
  reviewed: 2026-07-23 23:22:36
  approved: 2026-07-23 23:22:36
iteration: sprint-011
openspec_changes:
  - change_id: add-miniapp-sku-video-fullscreen-actions
    type: update
    status: archived
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags: []
readiness: Ready
readiness_notes: 五件套已补齐，并提供小程序 prototype 策略；未命中 admin 横切标签，Knowledge-base gate 为 N/A。验收已吸收小程序运行入口同步、DevTools/真机 evidence、分享路径与埋点不阻断等同域复盘要点。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/miniapp/context.md
  - review.md
expected_openspec_change: add-miniapp-sku-video-fullscreen-actions
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-24 16:01:52 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-sku-video-fullscreen-actions） |
| 2026-07-24 15:59:25 | /opsx-archive | Change `add-miniapp-sku-video-fullscreen-actions` 已归档，状态同步完成。 |
| 2026-07-23 23:58:05 | /opsx-apply | Change `add-miniapp-sku-video-fullscreen-actions` apply 进行中，待补齐剩余验收。 |
| 2026-07-23 23:36:24 | `/sprint-propose` | 纳入 sprint-011 正式范围，状态更新为 in_sprint |
| 2026-07-23 23:35:30 | `/req-opsx` | 修正未纳入 Sprint 的状态语义：保留 approved，等待后续 /sprint-propose |
| 2026-07-23 23:30:57 | `/req-opsx` | 创建 OpenSpec Change add-miniapp-sku-video-fullscreen-actions，状态 proposed |
| 2026-07-23 23:23:28 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-23 23:22:36 | `/req-review --approve` | 评审通过，状态更新为 approved，准备执行 plan → review 阶段迁移 |
| 2026-07-23 23:19:20 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与小程序 prototype 策略；无 admin 横切 AC；状态更新为 pending_review |
| 2026-07-23 23:15:48 | `/req-generate` | 生成 requirement.md，状态更新为 draft |
| 2026-07-23 23:11:09 | `/req-capture` | 记录小程序商品详情页视频全屏入口与全屏态长按操作菜单需求 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-24 15:59:25 workflow-sync：状态同步为 done（Change archived）
