---
bug_id: BUG-0110-miniapp-card-banner-thumbnail-usage
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 13:37:11
severity_hint: high
environment: miniapp-media-display
related_requirement: null
related_bug: BUG-0100-thumbnail-size-equals-original
lifecycle_stage: plan
captured_via: capture
classification_rationale: 小程序商品卡片、品牌卡片、证书卡片和 Banner 的缩略图加载策略已作为性能优化方向存在，用户要求核查并修复未按缩略图处理的场景，属于既有媒体加载策略可能未全量落地的 BUG。
---

# 现象

小程序商品卡片、品牌卡片、证书卡片和 Banner 应使用缩略图；需要判断是否全部按此逻辑处理，如有遗漏则修复。

# 复现步骤

1. 打开微信小程序。
2. 分别访问商品列表、品牌列表、证书列表和包含 Banner 的页面。
3. 查看卡片和 Banner 图片加载请求或渲染字段。
4. 判断是否使用缩略图 URL，而非原图 URL。

# 期望 vs 实际

- 期望：商品卡片、品牌卡片、证书卡片和 Banner 均优先使用缩略图，必要时才按既定降级策略使用原图或占位。
- 实际：当前尚未确认全部场景均按缩略图逻辑处理，若存在原图加载会造成性能回退。

# 影响范围

- 微信小程序商品卡片、品牌卡片、证书卡片。
- 微信小程序 Banner 图片展示。
- 媒体 URL 字段选择、缩略图降级策略与图片加载性能。

# 初步线索

- 需要检查各小程序页面和组件是否统一读取 thumbnail URL 字段。
- 需要确认品牌、证书、Banner 接口返回字段是否包含可用缩略图。
- 修复时应保留图片缺失、缩略图缺失或加载失败的降级策略。

# 建议验收或复现要点

- [ ] 商品卡片使用缩略图。
- [ ] 品牌卡片使用缩略图。
- [ ] 证书卡片使用缩略图。
- [ ] Banner 使用缩略图或符合性能策略的展示图。
- [ ] 缩略图缺失时按明确降级策略显示，不出现空白或报错。
- [ ] 不影响点击跳转、图片预览和详情页原图展示策略。

# 附件

- 暂无。
