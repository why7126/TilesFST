---
bug_id: BUG-0086-miniapp-sku-detail-remark-not-shown
title: 小程序商品详情页备注说明信息没有显示
severity: medium
status: done
owner: null
discovered_at: 2026-07-28 22:24:26
environment: miniapp
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-remark-display
created_at: 2026-07-28 22:29:49
updated_at: 2026-07-29 07:55:06
---

# 现象

微信小程序商品详情页中，商品或 SKU 已维护的备注说明信息没有显示出来，导致用户在详情页无法看到完整的商品补充说明。

# 复现步骤

1. 在管理端或数据源中准备一条已填写备注说明信息的商品/SKU。
2. 打开微信小程序。
3. 进入该商品/SKU 的商品详情页。
4. 查看详情页信息区是否展示备注说明内容。

# 期望结果

- 当商品/SKU 存在备注说明信息时，小程序商品详情页应展示对应内容。
- 当备注说明为空时，页面应按既有空态规则隐藏该信息区或显示合理占位，不应出现异常空白、布局错位或报错。

# 实际结果

商品/SKU 存在备注说明信息，但小程序商品详情页未展示该内容。

# 影响范围

- 微信小程序商品详情页：`src/miniapp/pages/tile-detail/`
- 商品/SKU 详情接口返回字段到小程序页面渲染的数据映射链路
- 商品资料完整展示体验
- `REQ-0044-miniapp-sku-detail-page` 中商品详情信息展示相关验收

# 严重等级说明

严重等级为 `medium`。该问题不会阻断商品详情页整体访问，但会造成商品补充说明信息缺失，影响店主或客户查看商品资料的完整性，需要进入常规修复流程。
