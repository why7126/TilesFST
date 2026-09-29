---
change_id: update-miniapp-price-red-display
requirement_id: REQ-0133-miniapp-price-red-display
created_at: 2026-09-05 22:20:40
updated_at: 2026-09-05 22:20:40
---

## 背景

REQ-0133已评审并纳入sprint-029。小程序价格沿用品牌金，用户希望金额更易识别；共享卡片和详情、推荐、收藏的独立价格节点需统一有效金额红色、无价及失效中性色。

## 变更内容

- 增加独立价格语义色和统一展示状态口径，保留既有price_display与价格计算。
- 覆盖首页、商品列表、品牌商品列表、搜索SKU卡片、详情主价格与推荐、收藏价格。
- 保持参考价格、单位说明、无价和失效文案层次，以及品牌金、按钮、其他端视觉。
- 同步UI规范、token、相关小程序回归及视觉证据；不改变API、DB、部署、分享、图片布局或媒体路径。

## 能力

### 新增能力

无独立新业务能力。

### 修改能力

- `design-system`：新增小程序价格语义色与跨入口展示状态要求，以ADDED条目补充已有能力，不复制各页面完整规格。

## 影响范围

主要影响src/miniapp共享商品卡片、详情与收藏的展示状态及WXSS，src/shared/design-system/tokens和必要的小程序token映射，rules/ui-design.md及相关说明、tests/test_miniapp_static.py和聚焦状态测试。Web只在共享token同步或Design System预览需要时涉及，无产品视觉改动；管理端、后端、数据库、对象存储无行为变化。Orval及Docker Compose验证为N/A。

## 分类与交付边界

类型为update：基于已交付能力的体验增强，不将原金色实现归类为缺陷。现有BUG-0148图片适配与本Change触及同一组件，实施需保持其成果。局部HTML原型已提供，PNG、Skeleton及实际视觉证据由实施阶段补齐。
