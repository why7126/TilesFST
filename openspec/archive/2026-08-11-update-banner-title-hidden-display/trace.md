---
change_id: update-banner-title-hidden-display
type: update
status: proposed
created_at: 2026-08-10 23:02:22
updated_at: 2026-08-11 23:15:05
source_requirement: REQ-0106-admin-banner-title-hidden
iteration: sprint-022
tasks_completed: 0
tasks_total: 17
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-11 23:15:05 | acceptance.real-device | 用户确认 REQ-0106 已完成小程序真机验收：首页与品牌列表页 Banner 有图场景不展示标题遮罩，点击跳转不回归，满足 AC-XCUT-010 端上来源证据。 |
| 2026-08-10 23:02:22 | req.opsx | 由 REQ-0106 创建 OpenSpec Change，进入 proposed。 |

## 原型与验收冲突

| 来源 | 冲突 | 处理 |
|---|---|---|
| `openspec/specs/web-client` | Banner 弹窗要求展示 Banner 标题 | 本 Change 改为隐藏标题字段，并自动生成内部标题 |
| `openspec/specs/web-client` | Banner 列表第一列要求缩略图与标题 | 本 Change 改为缩略图与投放上下文优先，标题仅内部识别 |
| `openspec/specs/miniapp-brand-list-page` | 品牌轮播要求展示标题 | 本 Change 改为有图 Banner 不展示 `title` 主标题 |
| `openspec/specs/banner-management` | 标题重复错误作为业务错误 | 本 Change 保留内部错误码，但用户可见提示不得要求运营修改标题 |
