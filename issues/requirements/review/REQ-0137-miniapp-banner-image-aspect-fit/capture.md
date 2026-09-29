---
req_id: REQ-0137-miniapp-banner-image-aspect-fit
status: captured
created_at: '2026-09-07 22:45:57'
updated_at: '2026-09-07 22:45:57'
recorded_by: product
source: 用户反馈与 /explore 分析
captured_via: capture
classification_rationale: 当前 BUG-0148 明确只覆盖 grid 商品卡片并排除 Banner、商品详情轮播和品牌图；本输入要求新增统一 Banner 图片完整适配展示规则，属于小程序视觉展示需求。
priority_hint: P1
parent_requirement: null
related_requirements:
- REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
product_data_collection_observability:
  applicability: not_applicable
  affected_layers:
  - wechat_miniapp
  reason: 本次 capture 仅记录小程序 Banner 图片显示模式与容器适配规则，预期不改变 API 字段、数据库、媒体 object key、对象存储策略、小程序请求封装、行为事件或 Task Trace；若后续设计扩大到接口字段、媒体变体策略或埋点，则需重新声明适用性。
  validation: capture 阶段基于现有 WXML/WXSS 只读定位完成；未执行实现、静态测试或真机截图验证。
---

# 一句话

小程序所有 Banner 图片展示策略调整为完整适配，优先保证图片 100% 显示。

# 原始描述

小程序所有 Banner 图片展示策略调整为完整适配，覆盖首页 Banner、品牌列表 Banner、品牌详情头图、商品详情顶部媒体图；图片优先 100% 完整显示，允许留白，视频和非 Banner 缩略图暂不纳入。

# 分类分析

| 条目 | 类型 | 理由 |
|---|---|---|
| 小程序 Banner 图片完整适配展示 | REQ | 这是对多个 Banner / 大图位建立新的统一展示规则；当前 `BUG-0148` 明确排除商品详情轮播、品牌图和 Banner 图，不属于原 BUG 修复范围内的验收返修。 |

# 范围建议

In：

- 首页 Banner 轮播图片。
- 品牌列表页 Banner 轮播图片。
- 品牌详情页头图。
- 商品详情页顶部媒体图中的图片项。
- 图片完整适配展示，允许上下或左右留白。
- 保持容器高度稳定，避免布局跳动、横向溢出、文字遮挡或图片拉伸。

Out：

- 视频展示策略。
- 商品推荐图、商品卡片非 Banner 缩略图。
- 证书图、品牌圆形 Logo 等非 Banner 图片。
- API 字段、数据库结构、媒体对象 key、对象存储策略和图片派生生成策略。

# 现有依据

- `src/miniapp/pages/index/index.wxml`：首页 Banner 轮播图片当前使用 `aspectFill`。
- `src/miniapp/pages/brand-list/index.wxml`：品牌列表 Banner 轮播图片当前使用 `aspectFill`。
- `src/miniapp/pages/brand-detail/index.wxml`：品牌详情头图当前使用 `aspectFill`。
- `src/miniapp/pages/tile-detail/index.wxml`：商品详情顶部媒体图中的图片项当前使用 `aspectFill`。
- `openspec/changes/fix-miniapp-product-grid-image-fit/proposal.md`：`BUG-0148` 不变范围明确排除商品详情页轮播、图片预览、品牌图、证书图和 Banner 图。

# 背景与价值

Banner / 大图位经常承载商品主体、品牌视觉和宣传文字。当前填充裁切策略能保持视觉铺满，但会在图片比例与容器比例不一致时裁掉边缘、文字或产品主体。对于瓷砖选型和品牌展示，完整露出图片信息比铺满容器更重要。

# 建议验收要点

- 首页 Banner、品牌列表 Banner、品牌详情头图、商品详情顶部媒体图片在常见手机宽度下均能完整显示图片主体，不裁切文字、边缘和产品主体。
- 图片展示允许留白，但不得拉伸变形、横向溢出、遮挡叠层文案或导致布局跳动。
- 视频和非 Banner 缩略图保持现状，不因本需求改变展示策略。
- 覆盖小程序静态测试，断言目标 Banner / 大图位图片使用完整适配展示模式。
- 使用微信 DevTools 或真机截图记录至少 320、375、430 pt 等价宽度的关键页面展示证据。

# 待澄清

- [ ] 确认“所有 Banner”是否仅限本 capture 的四类大图位。
- [ ] 确认品牌详情头图上的文字叠层在留白背景下是否保留，或是否需要调整遮罩/背景。
- [ ] 确认商品详情顶部媒体图的视频项是否后续另行评估完整适配。

# 影响与边界

本次仅 capture，不生成 PRD、不创建 OpenSpec Change、不实现代码。预期影响小程序展示层；不影响 API、数据库、Web、管理端、Orval、Docker Compose 或对象存储。后续若进入实现，应先完成 `/req-generate`、`/req-complete`、`/req-review`、`/sprint-propose` 与 `/req-opsx`。

# 规范依据

遵循 `rules/requirement-management.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、`rules/ui-design.md`、`rules/testing.md`、`rules/security.md`、`rules/agent-context-budget.md`。
