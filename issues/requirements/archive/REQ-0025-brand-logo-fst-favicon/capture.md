---
req_id: REQ-0025-brand-logo-fst-favicon
status: captured
created_at: 2026-07-01 20:47:03
updated_at: 2026-07-01 20:47:03
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0010-product-version-display
---

# 一句话

需要将产品品牌区调整为 Logo + “菲尚特FST” + 版本号 + “家居建材资料库”的结构，并将网页标签图标替换为同一产品 Logo，统一 Web 管理端品牌识别。

# 原始描述

品牌区改成Logo + “菲尚特FST“ + 版本号 + “家居建材资料库”的结构。网页图标也替换成Logo

# 背景与关联

- 父需求：`REQ-0010-product-version-display`
- 关联能力：管理端侧栏品牌区、产品版本号展示、网页 favicon / apple-touch-icon
- 影响范围：Web 管理端应用壳层、浏览器标签页图标
- 业务价值：统一从旧 `TILESFST` 文案向“菲尚特FST”品牌露出过渡，让侧栏品牌区与浏览器标签图标保持一致，提升品牌识别度。

# 待澄清

- [ ] 品牌区是否只覆盖管理端侧栏，还是同步覆盖登录页、店主 Web 展示端导航和 Design System 示例页
- [ ] “菲尚特FST”中的 FST 是否需要使用独立字重、颜色或英文副标样式
- [ ] 版本号位置是否固定在品牌主标题同行，收起态是否仍展示版本号
- [ ] favicon 是否直接使用原始 Logo 图片，还是需要导出 32x32 / 180x180 / maskable 等多尺寸图标
- [ ] 是否需要更新历史原型与旧文档中 `TILESFST` 品牌文案，或仅面向当前实现

# 探索结论

（/req-explore 后人工确认写入）

# 拆分说明

本次不拆分为多条 REQ：品牌区结构与网页图标替换同属产品品牌露出统一优化，Logo、品牌文案、版本号和 favicon 需要在同一视觉验收闭环中确认。
