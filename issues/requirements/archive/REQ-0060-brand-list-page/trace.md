---
requirement_id: REQ-0060-brand-list-page
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-19 22:26:11
updated_at: 2026-07-20 22:48:26
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0060-brand-list-page
requirement_name: brand-list-page
requirement_type: 品牌浏览 / 侧边栏导航
priority: P1
status: done
owner: product
source: 用户反馈
target_clients:
  web_admin: 待确认
  web_catalog: 待确认
  wechat_miniapp: 待确认
related_requirements:
  - REQ-0005-brand-management
related_changes:
  - add-brand-list-page
lifecycle:
  captured: 2026-07-19 22:26:11
  generated: 2026-07-19 23:12:10
  completed: 2026-07-19 23:28:20
  reviewed: 2026-07-19 23:45:58
  approved: 2026-07-19 23:45:58
iteration: sprint-009
openspec_changes:
  - change_id: add-brand-list-page
    type: add
    status: archived
readiness: Ready
readiness_notes: 五件套已补齐；UI 原型策略已提供 prototype/miniapp/context.md 与 prototype.html，PNG 待后续导出但不阻塞评审。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
  - prototype/miniapp/context.md
  - prototype/miniapp/prototype.html
knowledge_base_refs:
  - docs/knowledge-base/README.md
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags: []
ui_quality_tags:
  - miniapp-navigation
  - miniapp-device-evidence
expected_openspec_change: add-brand-list-page
```

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0005-brand-management | parent | 品牌主数据、Logo、启停和公开展示基础 |
| REQ-0041-miniapp-home | related | 品牌页轮播对齐小程序首页轮播体验 |
| REQ-0054-brand-card-common-component | related | 品牌卡片展示逻辑参考；双列列表态可能扩展样式 |
| REQ-0058-brand-detail-home-page | related | 品牌卡片跳转目标与品牌详情页/主页对齐 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---|
| admin-list | N/A | 0 |
| admin-form | N/A | 0 |
| admin-modal | N/A | 0 |
| media-upload | N/A | 0 |
| miniapp-navigation（非 req-complete admin 横切标签） | docs/knowledge-base/best-practices/miniapp-custom-navigation.md | 5 |

说明：本 REQ 为微信小程序访客端品牌列表页，不命中 `req-complete` 规定的管理端横切标签；因此管理端 knowledge-base gate 为 N/A。由于涉及小程序页面顶部、入口和设备视口验收，已读取并转化小程序自定义导航 best-practice。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 22:48:05 | lifecycle-stage-migrate | review → archive（/opsx-archive add-brand-list-page） |
| 2026-07-20 22:46:24 | /opsx-archive | Change `add-brand-list-page` 已归档，状态同步完成。 |
| 2026-07-20 08:12:49 | `/sprint-propose` | 纳入 `sprint-009` 正式范围，关联 Change `add-brand-list-page` |
| 2026-07-20 00:24:08 | `/req-opsx` | 修正未纳入 Sprint 的状态语义：保留 approved，等待后续 /sprint-propose |
| 2026-07-20 00:15:10 | `/req-opsx` | 创建 OpenSpec Change `add-brand-list-page`，状态 proposed |
| 2026-07-19 23:52:37 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 23:45:58 | `/req-review --approve` | 需求评审通过，状态更新为 approved，准备迁移至 review 阶段目录 |
| 2026-07-19 23:28:20 | `/req-complete` | 补齐 user-stories、business-flow、acceptance 与 prototype/miniapp；读取 sprint-008 复盘和小程序自定义导航 best-practice，状态更新为 pending_review |
| 2026-07-19 23:12:10 | `/req-generate` | 生成品牌列表页 requirement.md，状态更新为 draft |
| 2026-07-19 22:26:11 | `/req-capture` | 记录新增品牌列表页，并将侧边栏“找砖”入口文案调整为“品牌” |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-20 22:46:24 workflow-sync：状态同步为 done（Change archived）
