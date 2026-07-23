---
bug_id: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
title: 生产环境小程序商品详情页品牌卡片误跳搜索页
status: done
created_at: 2026-07-21 10:29:03
updated_at: 2026-07-22 09:00:40
severity_hint: medium
environment: prod
source: 用户反馈
source_command: /bug-capture
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug:
---

# 现象

生产环境微信小程序中，商品详情页「商品参数」区域的品牌卡片点击后跳转到搜索页，而不是品牌详情页。

# 复现步骤

1. 打开生产环境微信小程序。
2. 进入任意包含品牌信息的商品详情页。
3. 在商品详情页找到「商品参数」区域。
4. 点击「品牌」卡片。
5. 观察跳转后的页面。

# 期望 vs 实际

期望：点击「商品参数」中的品牌卡片后，跳转到对应品牌详情页，并展示该品牌信息及相关商品。

实际：点击品牌卡片后跳转到搜索页，未进入品牌详情页。

# 附件

- 用户原始反馈：`生产环境的微信小程序，商品详情页，点击商品参数的 品牌卡片，跳转至 搜索页，而非品牌详情页`
- 关联需求：`REQ-0044-miniapp-sku-detail-page`
- 暂无截图、具体商品 SKU、品牌 ID 与页面路径；后续 `/bug-explore` 阶段需补充。
