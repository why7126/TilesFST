---
bug_id: BUG-0110-miniapp-card-banner-thumbnail-usage
title: 小程序卡片与 Banner 可能未统一使用缩略图
severity: high
status: done
owner:
discovered_at: 2026-08-03 08:13:39
environment: miniapp-media-display
related_requirement: null
related_change: fix-miniapp-card-banner-thumbnail-usage
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 13:36:58
---

# 小程序卡片与 Banner 可能未统一使用缩略图

## 现象

小程序商品卡片、品牌卡片、证书卡片和 Banner 应优先使用缩略图展示。当前需要核查这些场景是否全部按缩略图策略取图；若仍有场景直接加载原图，会造成列表页、卡片页或首页 Banner 的图片加载性能回退。

## 复现步骤

1. 打开微信小程序。
2. 分别访问商品列表、品牌列表、证书列表和包含 Banner 的页面。
3. 检查卡片和 Banner 图片渲染字段，或通过网络请求观察图片资源 URL。
4. 确认展示图是否优先使用缩略图 URL，而不是原图 URL。
5. 在缩略图字段缺失、为空或加载失败时，确认页面是否按既定降级策略展示原图或占位图。

## 期望结果

- 商品卡片、品牌卡片、证书卡片和 Banner 均优先使用缩略图。
- 缩略图不可用时，按明确降级策略展示原图或占位图。
- 图片字段选择不影响点击跳转、图片预览和详情页原图展示策略。

## 实际结果

当前尚未确认全部小程序卡片和 Banner 场景均已使用缩略图。若存在遗漏场景直接使用原图，会导致移动端图片体积过大、首屏或列表加载变慢，并与既有缩略图性能策略不一致。

## 影响范围

- 微信小程序商品卡片图片展示。
- 微信小程序品牌卡片图片展示。
- 微信小程序证书卡片图片展示。
- 微信小程序 Banner 图片展示。
- 媒体 URL 字段选择、缩略图降级策略与图片加载性能。

## 严重等级说明

严重等级为 `high`。该问题影响小程序多个高频图片展示场景，可能造成移动端加载性能明显回退，并与 `BUG-0100-thumbnail-size-equals-original` 相关的缩略图治理目标存在关联；但目前尚未确认导致功能不可用或数据损坏，因此未定为 `critical` 或 `blocker`。
