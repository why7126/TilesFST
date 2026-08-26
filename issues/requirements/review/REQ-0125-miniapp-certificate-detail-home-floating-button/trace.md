---
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
status: in_sprint
lifecycle_stage: review
priority: P2
created_at: 2026-08-25 22:30:50
updated_at: 2026-08-26 08:34:40
lifecycle:
  captured: 2026-08-25 22:30:50
  generated: 2026-08-25 22:35:40
  completed: 2026-08-25 22:39:27
  reviewed: 2026-08-25 22:43:55
  approved: 2026-08-25 22:43:55
iteration: sprint-026
openspec_changes:
  - change_id: update-miniapp-certificate-detail-home-floating-button
    type: update
    status: applied
related_requirements:
  - REQ-0085-miniapp-global-home-floating-button
  - REQ-0080-miniapp-certificate-detail-page
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
related_changes:
  - update-miniapp-certificate-detail-home-floating-button
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
requirement_name: miniapp-certificate-detail-home-floating-button
requirement_type: 小程序 / 页面体验 / 导航一致性
priority: P2
status: in_sprint
owner: product
source: 用户反馈
target_clients:
  wechat_miniapp: 本期
  web_admin: 不适用
  web_catalog: 不适用
  backend_api: 不适用
related_requirements:
  - REQ-0085-miniapp-global-home-floating-button
  - REQ-0080-miniapp-certificate-detail-page
related_changes:
  - update-miniapp-certificate-detail-home-floating-button
lifecycle:
  captured: 2026-08-25 22:30:50
  generated: 2026-08-25 22:35:40
  completed: 2026-08-25 22:39:27
  reviewed: 2026-08-25 22:43:55
  approved: 2026-08-25 22:43:55
iteration: sprint-026
openspec_changes:
  - change_id: update-miniapp-certificate-detail-home-floating-button
    type: update
    status: applied
readiness: Ready
readiness_notes: 已补齐 requirement.md、user-stories.md、business-flow.md、acceptance.md、trace.md 与 prototype/miniapp/prototype-context.md；无 admin/media 强制横切标签。
cross_cutting_tags:
  - miniapp
  - certificate-detail
  - home-floating-button
  - navigation
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-025-retrospective.md
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/prototype-context.md
expected_openspec_change:
```

## 知识库横切报告

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 | 说明 |
|---|---|---:|---|
| 无匹配强制标签 | - | 0 | 不属于 `admin-list`、`admin-form`、`admin-modal` 或 `media-upload`。 |
| miniapp-navigation | `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 5 | 非强制横切标签；已转为 `AC-NAV-*`，覆盖分享直达、返回兜底、页面 offset、截图矩阵和导航锁恢复。 |
| sprint-025-retrospective | `docs/knowledge-base/retrospectives/sprint-025-retrospective.md` | 1 | 复盘提示小程序新增媒体位需证据化验收；本需求转化为静态检查和 DevTools evidence 要求。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 23:26:15 | /opsx-modify | Change `update-miniapp-certificate-detail-home-floating-button` 验收返修已同步，待复验或 archive。 |
| 2026-08-25 23:04:35 | /opsx-apply | Change `update-miniapp-certificate-detail-home-floating-button` apply 进行中，待补齐剩余验收。 |
| 2026-08-25 22:47:06 | `/sprint-propose` | 纳入 `sprint-026` 正式范围，估算 XS / 0.5 人天；待 `/req-opsx` 创建 OpenSpec Change |
| 2026-08-25 22:44:29 | lifecycle-stage-migrate | plan → review（/req-review） |
| 2026-08-25 22:43:55 | `/req-review` | 需求评审通过，状态更新为 approved，准备迁移至 review 阶段 |
| 2026-08-25 22:39:27 | `/req-complete` | 补齐用户故事、业务流程、验收标准和小程序原型上下文；引用小程序自定义导航最佳实践，状态更新为 pending_review |
| 2026-08-25 22:35:40 | `/req-generate` | 根据 capture 生成证书详情页返回首页悬浮按钮 PRD，明确 offset 与其他页面保持一致 |
| 2026-08-25 22:30:50 | `/capture` | 记录小程序证书详情页新增返回首页悬浮按钮需求 |
