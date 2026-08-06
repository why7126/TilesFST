---
change_id: fix-miniapp-privacy-interface-drift
capability: miniapp-home
created_at: 2026-08-05 14:42:11
updated_at: 2026-08-05 14:42:11
---

## MODIFIED Requirements

### Requirement: 分享与咨询

小程序首页和商品详情 SHALL 支持微信原生分享，并 SHALL 提供不触发电话或剪贴板隐私接口的门店服务展示能力。门店服务动作 SHALL 与当前产品隐私声明一致，不得要求声明电话拨打或剪贴板能力。

#### Scenario: 分享商品

- **WHEN** 用户在商品详情页触发分享
- **THEN** 小程序 SHALL 使用微信原生分享或等价分享入口
- **AND** 分享路径 SHOULD 回到对应商品详情页
- **AND** 系统 SHALL 记录商品分享行为。

#### Scenario: 门店服务不触发电话或剪贴板

- **WHEN** 用户打开首页服务区、门店信息页或商品详情页中的门店服务入口
- **THEN** 小程序 SHALL NOT 调用 `wx.makePhoneCall`
- **AND** 小程序 SHALL NOT 调用 `wx.setClipboardData`
- **AND** `GET /api/v1/miniapp/home` 的 `services[].action_type` SHALL NOT 返回 `phone`
- **AND** `GET /api/v1/miniapp/home` 的 `services[].action_type` SHALL NOT 返回 `copy_wechat`
- **AND** 缺少安全动作的咨询方式 SHALL 隐藏、展示为无动作服务说明，或使用非隐私接口的稳定提示安全降级
- **AND** 系统 SHALL 记录不含手机号、微信号、剪贴板内容或其它个人隐私原文的服务行为事件。
