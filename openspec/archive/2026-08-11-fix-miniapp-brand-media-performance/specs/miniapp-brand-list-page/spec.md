# miniapp-brand-list-page Delta

## MODIFIED Requirements

### Requirement: 品牌列表页轮播
品牌列表页 SHALL 在顶部提供品牌轮播区域，并 SHALL 与小程序首页轮播保持一致的基础交互体验。品牌轮播区域 SHALL NOT 展示开发、原型、验收或能力说明类文案作为正式用户可见内容。品牌轮播图片 SHALL 优先使用后端受控真实轻量缩略图；缩略图缺失或加载失败时 SHALL 安全回退原图或品牌化兜底图。

#### Scenario: 品牌轮播图片优先使用轻量缩略图

- **WHEN** 品牌列表页展示品牌轮播图片
- **THEN** 小程序 SHALL 优先使用后端返回的缩略图 URL 或等价轻量展示 URL
- **AND** 缩略图对象 SHALL 真实存在，且字节数或像素尺寸应明显小于原图
- **AND** `.thumb` URL 实际回退原图时 SHALL 记录为性能风险
- **AND** 页面 SHALL NOT 仅因 URL 包含 `.thumb` 就判定图片性能验收通过。

### Requirement: 双列品牌卡片列表

品牌列表页 SHALL 在顶部轮播或品牌氛围 Hero 下方以每行一个品牌的信息卡片展示公开可见品牌，并 SHALL 为 Logo、长品牌名、商品数量、末级类目胶囊、不可用品牌和小屏视口提供稳定降级。品牌 Logo 或品牌图片小图 SHALL 优先使用后端受控真实缩略图；缩略图缺失或加载失败时 SHALL 安全回退原图、品牌首字或统一占位。非首屏品牌卡片图片 SHALL 启用小程序懒加载或等价延迟加载策略。

#### Scenario: 品牌卡片图片懒加载与缩略图收益验收

- **WHEN** 品牌列表页展示多条品牌卡片
- **THEN** 品牌卡片 Logo 或品牌图片 SHALL 优先使用真实轻量缩略图
- **AND** 非首屏品牌卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 首屏关键品牌图片 SHALL 保持可预期展示，不得因懒加载造成明显空白
- **AND** 图片加载失败时 SHALL 使用原图、品牌首字或统一占位安全降级
- **AND** 小程序 evidence SHALL 覆盖品牌卡片图片 URL、资源大小、耗时、占位和失败态。
