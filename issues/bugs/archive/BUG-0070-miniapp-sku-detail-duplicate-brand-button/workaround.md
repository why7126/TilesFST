---
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
status: done
created_at: 2026-07-21 08:16:46
updated_at: 2026-07-22 08:30:50
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-duplicate-brand-button
---

# Workaround - BUG-0070 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复

## 临时规避方案

暂无需要对用户发布的临时规避方案。

在修复前，用户仍可通过以下任一入口进入品牌主页：

- 内容区“查看品牌主页”入口。
- 底部品牌按钮。

由于两个入口均为前端重复交互，且品牌主页仍可访问，本缺陷不需要后台数据修复、配置调整或运维干预。

## 运维 / 客服说明

如用户反馈底部品牌按钮重复，可说明：

1. 当前品牌主页访问能力可用。
2. 推荐使用内容区“查看品牌主页”入口。
3. 底部重复按钮会在后续修复中删除。

## 风险

临时不处理不会导致数据损坏或权限风险，但会持续影响 SKU 商品详情页底部操作区的清晰度。
