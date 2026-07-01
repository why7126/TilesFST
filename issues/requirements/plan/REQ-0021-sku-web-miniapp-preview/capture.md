---
req_id: REQ-0021-sku-web-miniapp-preview
status: captured
created_at: 2026-06-30 11:34:04
updated_at: 2026-06-30 11:34:04
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0006-tile-sku-management
captured_via: capture
classification_rationale: 新增商品后需要 Web 与小程序视图预览，属于 SKU 上线前确认效果的新工作流能力。
---

# 一句话

新增或编辑商品/SKU 后，管理端应提供小程序视图与 Web 视图预览能力，方便用户在上线 SKU 前立即确认展示效果。

# 原始描述

加完商品后，建议加上小程序、web 视图的预览功能，方便用户在上线 SKU 时立马知道这个效果。

# 背景与关联

- 父需求：`REQ-0006-tile-sku-management`
- 涉及端：Web 管理端、小程序展示视图、Web 展示端
- 业务价值：降低 SKU 上线后展示效果不符合预期的风险，支持运营在发布前自检图片、规格、价格、视频、文案等展示效果
- 预期后续：需要明确预览入口、预览数据来源、未发布 SKU 的访问控制，以及 Web/小程序预览样式与真实展示页一致性

# 待澄清

- [ ] 预览入口是在商品保存后弹出、详情页按钮、列表行操作，还是发布前确认流程中展示
- [ ] 小程序预览是二维码扫码预览、内嵌模拟器视图，还是生成可分享的受控预览链接
- [ ] Web 预览是否允许打开未发布 SKU 的临时预览链接
- [ ] 预览应覆盖哪些字段：主图、详情图、视频、规格、价格、上下架状态、品牌、分类、库存/询价入口等
- [ ] 预览链接是否需要权限、有效期和访问日志

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述上线 SKU 前新增 Web / 小程序展示预览能力，当前没有明确交付基线，因此判定为 REQ。
