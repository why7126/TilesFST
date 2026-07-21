---
review_id: REV-REQ-0058-001
requirement_id: REQ-0058-brand-detail-home-page
date: 2026-07-19
participants: []
result: approved
created_at: 2026-07-19 23:45:40
updated_at: 2026-07-19 23:45:40
---

# 需求评审

## 评审结论

`REQ-0058-brand-detail-home-page` 评审通过。

本需求已将范围明确收敛为微信小程序品牌入口页与品牌主页/详情页，覆盖品牌轮播、品牌双列卡片、品牌信息展示、商品 Tab、证书 Tab、加载/空态/错误态、导航与设备视口验收。需求文档、用户故事、业务流程、验收标准、trace 与小程序原型策略均已具备，满足进入 `/req-opsx` 与后续 Sprint 规划的前置条件。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类：原型或实现策略已决。
- [x] 无与现有 REQ 重复未说明。

## 条件通过项

- [ ] 后续 `/req-opsx` 生成 Change 时，必须显式说明品牌轮播优先复用首页轮播和现有 Banner 管理能力；若需新增 Banner 展示端/位置，必须同步 API、OpenAPI、Orval、docs 和 tests。
- [ ] 后续实现商品 Tab 时，必须复用或对齐 `REQ-0056-product-list-card-only-layout` 的双列商品卡片策略，不重复引入不一致的商品卡片结构。
- [ ] 后续实现证书 Tab 时，必须复用或对齐 `REQ-0038-brand-certificate-management` 与 `REQ-0057-certificate-list-page` 的证书展示边界，仅展示可公开证书。
- [ ] 后续验收必须覆盖 DevTools 320 / 375 / 430 pt 视口下品牌轮播、品牌卡片、Tab、商品卡片、证书卡片、自定义导航和底部 TabBar 不重叠。
- [ ] 若真机验收不可用，必须按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 标记 blocked 或 follow_up，不得写作真机通过。
