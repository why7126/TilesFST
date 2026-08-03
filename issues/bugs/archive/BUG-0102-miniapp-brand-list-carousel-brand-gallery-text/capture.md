---
bug_id: BUG-0102-miniapp-brand-list-carousel-brand-gallery-text
status: done
created_at: 2026-08-02 11:41:24
updated_at: 2026-08-02 16:51:05
severity_hint: low
environment: miniapp-brand-list
related_requirement: REQ-0060-brand-list-page
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 小程序品牌列表页与轮播图能力已交付，用户要求删除轮播图上出现的固定文案“BRAND GALLERY”，并强调轮播图保持现有品牌页能力；这是既有页面展示内容不符合预期的偏差，属于 BUG。
---

# 现象

小程序品牌列表页轮播图区域展示了不需要的固定文案 `BRAND GALLERY`。

# 复现步骤

1. 打开微信小程序。
2. 进入品牌列表页。
3. 查看页面顶部或品牌列表页轮播图区域。
4. 观察轮播图中是否显示 `BRAND GALLERY` 文案。

# 期望 vs 实际

- 期望：品牌列表页轮播图不显示 `BRAND GALLERY` 文案，页面只保留当前品牌页轮播图应有的图片展示与交互能力。
- 实际：轮播图区域仍显示 `BRAND GALLERY` 文案，影响品牌列表页展示简洁性。

# 影响范围

- 微信小程序品牌列表页。
- 品牌列表页轮播图视觉展示。
- 现有轮播图图片展示、切换、跳转或其他品牌页能力不应被本次修复改变。

# 初步线索

- 需要检查小程序品牌列表页轮播图模板或组件中是否存在硬编码 `BRAND GALLERY`。
- 需要确认该文案是否来自品牌页 Banner/轮播图配置、默认占位文案或样式层叠。
- 修复时应只移除该文案展示，不调整轮播图数据来源、图片展示逻辑和既有交互能力。

# 建议验收或复现要点

- [ ] 品牌列表页轮播图不再展示 `BRAND GALLERY` 文案。
- [ ] 轮播图图片仍按现有品牌页能力正常加载、展示和切换。
- [ ] 轮播图原有点击、跳转或关联品牌页能力保持不变。
- [ ] 文案删除后轮播图布局无空白占位、错位、遮挡或高度异常。
- [ ] 小程序真机或开发者工具中完成品牌列表页回归验证。

# 附件

- 暂无。
