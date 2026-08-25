---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
title: 小程序证书详情页顶部展示缺少 display_url 导致退回原图
severity: high
status: done
owner:
discovered_at: 2026-08-22 20:38:13
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_change: fix-miniapp-certificate-detail-display-url
updated_at: 2026-08-25 14:53:29
created_at: 2026-08-22 21:27:27
---

# 小程序证书详情页顶部展示缺少 display_url 导致退回原图

## 现象

小程序证书详情页顶部展示缺少可直接消费的 `display_url`。当详情展示缺少合适展示图字段时，页面存在直接回退到证书原图的风险。

## 复现步骤

1. 打开包含图片证书的小程序证书详情页。
2. 查看证书详情接口返回字段，确认是否存在 `display_url`。
3. 检查详情页顶部展示使用的图片 URL。
4. 在 Network 面板观察顶部证书图是否请求原图资源。

## 期望结果

- 证书详情接口返回可用于详情顶部展示的 `display_url`。
- 证书详情页顶部展示优先使用 `display_url`。
- 当 `display_url` 缺失时，页面采用受控展示策略或占位，不应无条件退回大体积原图。
- 图片证书、PDF/文档证书均有明确展示行为。

## 实际结果

- 证书详情顶部展示缺少 `display_url` 消费入口。
- 详情页顶部图片展示存在直接使用证书原图的风险。
- 普通详情浏览可能请求证书原图大文件，影响加载性能和原图访问流量。

## 影响范围

- 微信小程序证书详情页顶部图片展示。
- 证书详情 API 返回结构。
- 证书图片展示图、缩略图、原图的选择策略。
- 证书原图访问流量与详情页加载性能。

## 严重等级说明

严重等级为 `high`。该问题影响小程序证书详情页核心展示链路，并可能导致普通详情浏览请求大体积原图，带来加载性能退化和原图访问流量增加；同时它与媒体多规格展示策略相关，若接口字段和前端展示策略不统一，后续证书展示能力容易继续产生回退漂移。
openspec_changes:
  - change_id: fix-miniapp-certificate-detail-display-url
    type: fix
    status: archived
