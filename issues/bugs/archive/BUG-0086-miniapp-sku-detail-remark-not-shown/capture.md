---
bug_id: BUG-0086-miniapp-sku-detail-remark-not-shown
status: done
created_at: 2026-07-28 22:24:26
updated_at: 2026-07-29 07:55:06
severity_hint: medium
environment: miniapp
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 已有小程序商品详情页应展示商品详情信息，备注说明信息未显示属于既有能力/验收预期下的展示偏差，判定为 BUG。
---

# 现象

微信小程序商品详情页中，商品的备注说明信息没有显示出来。

# 复现步骤

1. 在管理端或数据源中准备一个带有备注说明信息的商品/SKU。
2. 打开微信小程序商品详情页。
3. 查看详情页信息区是否展示该商品/SKU 的备注说明内容。

# 期望 vs 实际

- 期望：小程序商品详情页应展示商品/SKU 已维护的备注说明信息；为空时可按既有空态规则隐藏或显示占位。
- 实际：商品/SKU 存在备注说明信息，但小程序详情页未显示该信息。

# 影响范围

- 微信小程序商品详情页：`src/miniapp/pages/tile-detail/`
- 商品/SKU 详情接口返回字段到小程序页面渲染链路
- 商品资料完整展示体验
- 与 `REQ-0044-miniapp-sku-detail-page` 的详情信息展示验收相关

# 初步线索

- 需确认后端详情接口是否已返回备注说明字段。
- 需确认小程序详情页数据映射是否遗漏备注说明字段。
- 需确认页面模板是否缺少备注说明展示区，或字段命名与接口返回不一致。

# 建议验收或复现要点

- 使用一条明确填写了备注说明的商品/SKU 数据进行复现。
- 验证接口响应中是否包含备注说明字段及字段值。
- 验证小程序详情页能展示非空备注说明；备注为空时不产生异常空白或布局错位。
- 覆盖微信开发者工具和至少一次真机预览验证。

# 附件

暂无。
