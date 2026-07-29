---
req_id: REQ-0080-miniapp-certificate-detail-page
status: done
created_at: 2026-07-29 07:57:17
updated_at: 2026-07-29 09:22:12
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0038-brand-certificate-management
captured_via: capture
classification_rationale: 用户提出“微信小程序新增证书详情页，参照商品详情页进行设计”，属于小程序证书展示链路的新页面能力；未提供已交付页面偏离验收的证据，因此判定为 REQ。
---

# 一句话

微信小程序新增证书详情页，并参照商品详情页的信息层级、视觉结构与浏览体验进行设计。

# 原始描述

微信小程序新增证书详情页，参照商品详情页进行设计

# 背景与关联

- 父需求：`REQ-0038-brand-certificate-management`
- 关联需求：`REQ-0057-certificate-list-page`、`REQ-0078-certificate-multiple-images-main-image`、`REQ-0044-miniapp-sku-detail-page`
- 涉及端：微信小程序
- 业务价值：让用户从证书列表、品牌详情或其他入口进入后，可以查看证书图片、名称、所属品牌、有效信息和说明内容，提升品牌资质可信度与浏览闭环。
- 预期后续：需要明确详情页入口、路由参数、接口数据字段、证书多图展示、主图优先规则、空状态/失效状态和真机验收范围。

# 待澄清

- [ ] 证书详情页入口来源：证书列表页、品牌详情页证书区域、商品详情页品牌/证书模块，还是多入口同时支持。
- [ ] 页面信息范围：证书名称、所属品牌、证书编号、发证机构、有效期、说明、图片组、更新时间等字段是否全部展示。
- [ ] 参照商品详情页的具体设计范围：顶部轮播、内容分区、品牌卡片、底部操作区、分享能力、导航栏标题等哪些需要复用。
- [ ] 多图证书在详情页是否按主图优先轮播展示，是否支持图片预览、长按保存或分享。
- [ ] 证书下架、无图片、图片加载失败、证书不存在时的提示和返回策略。
- [ ] 是否需要新增或复用现有证书详情 API；若 API 字段不足，后续 Change 需同步 OpenAPI、Orval/小程序服务层与测试。

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述小程序新增证书详情页，是对品牌证书公开展示链路的能力补齐；当前没有明确交付基线或异常复现步骤，因此不按 BUG 处理。
