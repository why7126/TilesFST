---
created_at: '2026-09-08 18:35:34'
updated_at: '2026-09-08 18:35:34'
---

## 背景

REQ-0137-miniapp-banner-image-aspect-fit 已评审并纳入 sprint-030。四类小程序大图当前填充裁切可能隐藏图片边缘，需按已评审需求完整适配、允许留白并维持容器稳定。

## 变更内容

- 首页Banner、品牌列表Banner、品牌详情头图、商品详情顶部图片等比完整适配，覆盖展示图和缩略图回退。
- 品牌详情在既有总高内分离图片和文字区域，保持品牌字段和截断语义。
- 保持加载、空态、错误回退、轮播、跳转和预览行为，补齐静态与视觉验收证据。

## 能力

### 新增能力

无。

### 修改能力

- `miniapp-home`：首页Banner完整适配。
- `miniapp-brand-list-page`：品牌轮播完整适配。
- `miniapp-brand-detail-home-page`：品牌头图与文字分区。
- `miniapp-sku-detail-page`：媒体图片完整适配，视频隔离。

## 影响范围

预期仅修改小程序四页面WXML/WXSS和聚焦测试。视频、非Banner图片、媒体URL/变体、API、数据库、Web、管理端及存储策略不变，无Orval或Docker Compose验证需求。分类为fix：修正既有展示与新评审视觉要求之间的差异；不扩大到BUG-0148的grid卡片。

产品数据采集与链路观测为not_applicable，affected_layers=[wechat_miniapp]；仅渲染布局，不新增请求、行为事件、日志、Task Trace或保留周期。后续以REQ的AC-OBS-001/002检查差异边界。
