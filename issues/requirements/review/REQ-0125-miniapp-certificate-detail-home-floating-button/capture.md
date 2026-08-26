---
req_id: REQ-0125-miniapp-certificate-detail-home-floating-button
status: captured
created_at: 2026-08-25 22:30:50
updated_at: 2026-08-25 22:30:50
recorded_by: product
source: 用户反馈
priority_hint: P2
parent_requirement: REQ-0085-miniapp-global-home-floating-button
captured_via: capture
classification_rationale: 证书详情页当前未配置明确的 home-floating-button，用户提出的是新增页面级悬浮返回首页入口，属于体验一致性增强需求而非已交付能力偏差。
---

# 一句话

小程序证书详情页需要新增【返回首页】悬浮按钮，与商品详情页、品牌详情页、商品列表页等二级页面保持一致的回首页体验。

# 原始描述

用户反馈：

```text
证书详情页新增【返回首页】悬浮按钮
```

# 背景与关联

- 关联父需求：`REQ-0085-miniapp-global-home-floating-button`
- 相关页面能力：`REQ-0080-miniapp-certificate-detail-page`
- 当前只读梳理结论：`pages/certificate-detail/index` 已使用 `custom-navigation`，但未引入或挂载 `home-floating-button`。
- 参考一致性页面：商品详情页、品牌详情页、商品列表页、搜索结果页、分类页、品牌列表页、收藏页、证书列表页。

# 影响范围

- 小程序：影响 `pages/certificate-detail/index` 页面展示与交互。
- 组件：预期复用已有 `components/home-floating-button/`，不新增独立按钮样式。
- API：不涉及。
- 数据库：不涉及。
- Web / 管理端：不涉及。
- Orval：不需要。
- Docker Compose：不需要。

# 建议验收要点

- [ ] 证书详情页展示【返回首页】悬浮按钮，视觉和交互复用现有 `home-floating-button`。
- [ ] 点击按钮优先通过 `wx.switchTab` 返回 `/pages/index/index`，失败时沿用组件内兜底策略。
- [ ] 按钮不遮挡证书主图、品牌入口卡片、证书信息和底部内容。
- [ ] 页面无数据、加载失败或分享直达等场景下仍可返回首页。
- [ ] 证书详情页原有左上返回能力保持可用。
- [ ] 小程序静态检查覆盖页面组件声明与 WXML 引用，避免 `.ts` 与 `.js` 实现漂移。

# 待澄清

- [ ] 悬浮按钮 offset 使用 `list`、`default` 还是其他更适合证书详情页内容结构的位置。
- [ ] 是否需要同步检查门店信息页等仍缺少显式悬浮按钮的页面。

# 探索结论

本条由 `/capture` 直接记录。前置 `/explore` 已确认：证书详情页属于注册页面，但没有明确的 `home-floating-button`；本需求作为单条小程序页面体验增强记录，不拆分。
