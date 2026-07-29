---
bug_id: BUG-0087-miniapp-brand-detail-product-tab-sort-order
status: done
created_at: 2026-07-28 22:29:01
updated_at: 2026-07-29 07:54:10
severity_hint: medium
environment: miniapp
related_requirement: REQ-0058-brand-detail-home-page
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 品牌详情页商品 Tab 属于已交付的小程序品牌详情能力，用户明确提出该 Tab 商品排序应按发布时间升序、ID 升序；现有/默认排序规则与期望展示顺序不一致，判定为既有能力偏差类 BUG。
---

# 现象

微信小程序品牌详情页商品 Tab 的商品排序需要按后端默认规则稳定展示为发布时间升序、ID 升序。

# 复现步骤

1. 准备同一品牌下多条已公开 SKU，确保发布时间或等价发布/更新时间不同。
2. 打开微信小程序品牌详情页。
3. 切换或查看商品 Tab。
4. 观察商品列表的返回顺序。

# 期望 vs 实际

- 期望：品牌详情页商品 Tab 的后端默认排序为发布时间升序、ID 升序，前端分页加载后保持该顺序展示。
- 实际：品牌详情页商品 Tab 当前排序规则待确认，可能未按发布时间升序、ID 升序返回与展示。

# 影响范围

- 微信小程序品牌详情页商品 Tab：`src/miniapp/pages/brand-detail/`
- 小程序公开商品列表接口：`/api/v1/miniapp/products`
- 后端品牌商品列表查询排序逻辑
- 与 `REQ-0058-brand-detail-home-page` 的品牌详情页商品展示体验相关

# 初步线索

- 品牌详情页商品 Tab 请求 `/api/v1/miniapp/products?brandId={brandId}&page={page}&pageSize={pageSize}`。
- 需确认后端默认排序字段中的“发布时间”对应 `published_at`、`created_at`、`updated_at` 或当前数据模型中的等价字段。
- 需确认同一发布时间下使用 `id ASC` 作为稳定兜底排序。

# 建议验收或复现要点

- 构造同品牌下多条发布时间不同的公开 SKU。
- 验证首屏与加载更多分页均按发布时间升序、ID 升序稳定返回。
- 验证不同品牌详情页商品 Tab 均遵循同一排序规则。
- 验证调整不影响搜索页相关性排序、新品榜、热销榜和普通商品列表既有排序策略，除非后续评审明确扩大范围。

# 附件

暂无。
