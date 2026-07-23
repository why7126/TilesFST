---
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
title: 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复
status: done
created_at: 2026-07-21 08:10:00
updated_at: 2026-07-22 08:30:50
severity_hint: medium
environment: 微信小程序
source: 用户反馈
source_command: /bug-capture
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug:
---

# 现象

微信小程序商品详情页底部存在品牌按钮，但页面内容区已经提供“查看品牌主页”入口，两个入口语义和跳转目标重复。用户反馈希望删除底部的品牌按钮，保留内容区入口。

# 复现步骤

1. 使用微信开发者工具或真机打开小程序。
2. 进入任意 SKU 商品详情页。
3. 查看页面内容区的“查看品牌主页”入口。
4. 查看页面底部操作区的品牌按钮。

# 期望 vs 实际

期望：商品详情页只保留一个清晰的品牌主页入口，底部操作区不再显示重复的品牌按钮。

实际：内容区已有“查看品牌主页”，底部仍显示品牌按钮，造成入口重复和底部操作区冗余。

# 附件

- 暂无截图或日志；后续 `/bug-explore` 阶段补充具体页面截图与品牌入口位置标注。
