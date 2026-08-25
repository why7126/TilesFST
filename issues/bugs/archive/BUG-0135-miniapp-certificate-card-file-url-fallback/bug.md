---
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
title: 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件
severity: high
status: done
owner:
discovered_at: 2026-08-22 20:38:13
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_change: fix-miniapp-certificate-card-file-url-fallback
updated_at: 2026-08-25 14:53:29
created_at: 2026-08-22 20:38:13
---

# 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件

## 现象

小程序证书卡在缺少缩略图时可能直接 fallback 到 `file_url` 原文件。证书卡属于列表、摘要或关联推荐等小尺寸展示位，若直接加载原文件，会让普通浏览场景承担原图或原始文件下载成本。

该行为与媒体多规格展示策略不一致：卡片场景应优先使用缩略图或受控占位，原文件只应在明确进入详情、预览或下载动作时访问。

## 复现步骤

1. 准备一条缺少证书缩略图但存在 `file_url` 的证书数据。
2. 打开展示该证书的卡片列表、品牌证书摘要或商品详情关联证书卡片。
3. 检查证书卡组件实际使用的图片来源字段。
4. 在微信小程序开发者工具 Network 面板中观察是否直接请求 `file_url` 原文件。

## 期望结果

- 证书卡有缩略图时优先使用缩略图展示。
- 证书卡缺少缩略图时展示占位图、文件类型占位或受控空态。
- 卡片展示场景不直接请求 `file_url` 原文件。
- 详情页或明确预览动作的展示策略与卡片 fallback 策略保持区分。
- 图片证书、PDF/文档证书、无预览资源证书均有明确占位状态。

## 实际结果

- 证书卡缺少缩略图时存在直接使用 `file_url` 的 fallback 风险。
- 卡片列表或摘要场景可能请求证书原图或原始文件。
- 在弱网或证书文件较大时，页面列表加载成本和对象存储流量会被放大。
- 原文件访问边界可能从详情/预览动作漂移到普通卡片展示。

## 影响范围

- 微信小程序证书卡片展示。
- 证书列表、品牌证书摘要、商品详情关联证书等卡片消费场景。
- 证书缩略图缺失时的占位和降级策略。
- 对象存储流量、移动端弱网体验和原文件访问控制边界。

## 严重等级说明

严重等级为 `high`。该问题发生在证书卡片这类可能批量渲染的展示位，一旦缺少缩略图就回退到原文件，会将原图或文档资源下载扩散到列表浏览场景，影响移动端加载性能、对象存储流量和原文件受控访问边界；同时它与 `REQ-0115-media-multi-variant-images` 的缩略图优先消费目标直接相关，需要在修复前明确记录。
openspec_changes:
  - change_id: fix-miniapp-certificate-card-file-url-fallback
    type: update
    status: archived
