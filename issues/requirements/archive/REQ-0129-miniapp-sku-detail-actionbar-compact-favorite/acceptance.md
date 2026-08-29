---
requirement_id: REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
acceptance_status: passed
created_at: 2026-08-28 13:37:34
updated_at: 2026-08-28 16:21:48
---

# 验收标准

## 功能 AC

- [ ] AC-001 商品详情页底部收藏按钮不再显示“收藏 / 已收藏”可见文字，仅保留心形图标或等价图标状态。
- [ ] AC-002 未收藏和已收藏状态可通过图标形态、颜色或等价视觉差异清晰区分。
- [ ] AC-003 点击收藏成功后，页面状态切换为已收藏，并展示成功反馈。
- [ ] AC-004 点击取消收藏成功后，页面状态切换为未收藏，并展示成功反馈。
- [ ] AC-005 收藏请求失败时，页面恢复到点击前状态，并展示失败反馈。
- [ ] AC-006 收藏请求中或 loading 态不导致底部操作栏高度跳变。
- [ ] AC-007 “分享给客户”按钮仍可调起微信原生分享能力，且按钮文案、主视觉权重和点击热区不被削弱。
- [ ] AC-008 商品详情页返回首页悬浮按钮在 actionbar 场景下完成 offset 调整，不遮挡收藏按钮、分享按钮或底部安全区。

## UI / 视觉 AC

- [ ] AC-009 底部操作栏整体高度相比当前纵向“图标 + 文字”结构明显压缩，并保留不小于 44x44 pt 或项目等价的有效触控区域。
- [ ] AC-010 320 pt、375 pt、430 pt 常见小程序视口下，底部操作栏无横向滚动、按钮挤压、文字裁切和视觉重叠。
- [ ] AC-011 带底部手势安全区设备下，底部操作栏和返回首页悬浮按钮均不贴边、不遮挡系统安全区。
- [ ] AC-012 收藏按钮图标大小、颜色和按压态延续商品详情页深色视觉风格，且视觉权重低于“分享给客户”主按钮。
- [ ] AC-013 不新增可见解释性文案替代被移除的“收藏 / 已收藏”第二行文字。

## 小程序导航与证据 AC

> 来源：`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`、`docs/knowledge-base/retrospectives/sprint-025-retrospective.md`

- [ ] AC-014 商品详情页按详情 / 分享直达页面形态验收返回兜底，不因底部栏或首页悬浮按钮调整影响返回首页能力。
- [ ] AC-015 视觉验收记录至少包含 DevTools 320 pt、375 pt、430 pt 的底部操作栏与首页悬浮按钮截图或人工摘要。
- [ ] AC-016 若无法完成真机验收，验收记录必须标记 `blocked` 或 `follow_up`，并说明剩余风险。
- [ ] AC-017 验收材料不得记录本机绝对路径、真实客户数据、密钥、Cookie、Authorization header 或 `.env` 内容。

## 产品数据采集与链路观测 AC

- [ ] AC-018 本需求声明 `product_data_collection_observability.status: not_applicable`，并写明 N/A 原因。
- [ ] AC-019 实现 diff 确认未修改小程序请求封装、收藏 API 路径、分享 API / 微信 `open-type`、track 事件名和数据模型。
- [ ] AC-020 若实现阶段实际新增或修改行为事件、请求字段、API、DB 或 Task Trace，必须重新打开产品数据采集与链路观测适用性评估，并同步补充对应验收项。

## 横切 AC（knowledge-base）

本 REQ 不命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 四类管理端横切标签，因此不新增 `AC-XCUT-*` 管理端横切验收项。小程序相关导航与证据要求已写入 AC-014 至 AC-017。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-28 16:13:12
accepted_by: workflow-sync
source_change: update-miniapp-sku-detail-actionbar-compact-favorite
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

