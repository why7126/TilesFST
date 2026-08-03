---
bug_id: BUG-0110-miniapp-card-banner-thumbnail-usage
created_at: 2026-08-03 08:22:59
updated_at: 2026-08-03 08:22:59
root_cause_status: suspected
category: code
related_requirement: null
related_bug: BUG-0100-thumbnail-size-equals-original
---

# 根因分析

## 直接原因

小程序商品卡片、品牌卡片、证书卡片和 Banner 的图片展示逻辑可能未统一使用缩略图 URL 字段。部分场景若仍读取原图 URL，会绕过既有缩略图性能策略。

## 根本原因

媒体展示字段选择缺少跨页面、跨组件的一致性约束。商品、品牌、证书和 Banner 属于不同展示场景，如果各自独立选择图片字段，容易出现某些组件已经使用缩略图、其他组件仍使用原图的实现漂移。

## 触发条件

- 小程序进入商品列表、品牌列表、证书列表或包含 Banner 的页面。
- 对应接口返回同时存在原图 URL 和缩略图 URL，或存在可降级的媒体字段。
- 展示组件未优先读取缩略图 URL，或缩略图缺失时没有执行明确降级策略。

## 分类

- 缺陷分类：`code`
- 影响层：微信小程序展示层、媒体 URL 字段选择、图片加载性能
- 关联缺陷：`BUG-0100-thumbnail-size-equals-original`

## 待确认项

- 商品卡片当前是否使用缩略图字段。
- 品牌卡片当前是否使用缩略图字段。
- 证书卡片当前是否使用缩略图字段。
- Banner 当前是否使用缩略图字段，或是否存在更适合 Banner 的性能图字段。
- 后端接口是否为品牌、证书和 Banner 返回了可用缩略图 URL。
