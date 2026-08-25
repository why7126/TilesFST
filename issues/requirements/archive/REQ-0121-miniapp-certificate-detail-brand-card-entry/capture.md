---
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
title: 小程序证书详情页品牌入口复用 brand-card
status: done
priority: P1
source: user
captured_via: capture
classification_rationale: 该输入描述证书详情页品牌入口的组件复用、接口字段补齐、埋点命名与图片轻量化目标，属于新增/调整能力诉求，未直接指向已交付能力偏差。
parent_requirement: REQ-0115-media-multi-variant-images
related_requirements:
  - REQ-0115-media-multi-variant-images
related_bugs:
  - BUG-0134-miniapp-certificate-detail-display-url
  - BUG-0137-miniapp-lightweight-image-variant-consumption
created_at: 2026-08-24 14:58:45
updated_at: 2026-08-24 17:08:44
---

# 小程序证书详情页品牌入口复用 brand-card

## 原始输入

小程序证书详情页所属品牌入口复用 brand-card 组件，并为证书详情 brand 数据补齐 `brand_logo_thumbnail_url`，统一品牌入口展示、跳转、埋点和图片轻量化策略。

埋点统一成 `brand_card_click`。

## 类型倾向

REQ。

## 背景

证书详情页需要展示所属品牌入口。该入口应与小程序其他品牌入口保持一致，复用既有 `brand-card` 组件能力，避免不同页面对品牌 Logo、跳转、埋点事件名和图片规格消费策略各自实现。

## 影响范围

- 小程序证书详情页所属品牌入口展示。
- 小程序 `brand-card` 组件复用边界。
- 证书详情接口或数据适配中的 `brand` 数据结构。
- 品牌 Logo 图片轻量化消费字段：`brand_logo_thumbnail_url`。
- 品牌入口点击跳转与埋点事件名：`brand_card_click`。

## 建议验收要点

- 证书详情页所属品牌入口复用小程序 `brand-card` 组件，展示样式、点击区域和跳转行为与其他品牌入口一致。
- 证书详情页 `brand` 数据补齐 `brand_logo_thumbnail_url`，组件优先消费缩略图字段；无缩略图时按既有轻量化降级策略处理，不直接扩大原图加载面。
- 点击证书详情页所属品牌入口后，跳转到对应品牌详情或既定品牌目标页。
- 所有 brand-card 点击埋点事件名统一为 `brand_card_click`，证书详情页不再使用页面专属或不一致事件名。
- 回归确认商品详情、品牌详情、证书详情等使用 `brand-card` 的入口展示、跳转与埋点口径一致。

## 待澄清项

- 无。
