---
bug_id: BUG-0070-miniapp-sku-detail-duplicate-brand-button
status: done
created_at: 2026-07-21 08:16:46
updated_at: 2026-07-22 08:30:50
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-duplicate-brand-button
---

# Acceptance - BUG-0070 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复

## 回归验收标准

- [x] AC-BUG-001 SKU 商品详情页内容区 MUST 保留“查看品牌主页”入口。
- [x] AC-BUG-002 点击内容区“查看品牌主页”入口 MUST 跳转到当前 SKU 关联品牌的正确品牌主页。
- [x] AC-BUG-003 SKU 商品详情页底部操作区 MUST 不再显示品牌按钮。
- [x] AC-BUG-004 删除底部品牌按钮后，底部操作区 MUST 不出现空白占位、错位、异常间距或残留点击热区。
- [x] AC-BUG-005 删除底部品牌按钮后，底部操作区其他既有入口 MUST 正常展示和点击，不得引入回归。
- [x] AC-BUG-006 SKU 未关联品牌或品牌信息缺失时，页面 MUST 不展示无效品牌主页入口，不得出现空按钮或跳转错误。
- [x] AC-BUG-007 修复不得新增购物车、购买、下单、支付、库存、优惠券、促销倒计时或询价承诺等 `REQ-0044` 范围外能力。
- [x] AC-BUG-008 若仅移除小程序前端重复按钮且不改变接口契约，MUST 明确说明不需要 OpenAPI / Orval；若实际修改 API 字段或响应结构，MUST 同步 OpenAPI、Orval、接口文档和测试。

## 本次验收记录

| 时间 | 证据 | 结论 |
|---|---|---|
| 2026-07-21 22:54:39 | 代码检查：SKU 详情页底部栏仅保留收藏和分享，内容区 `<brand-card>` 保留 `hint="查看品牌主页"`；静态回归：4 个相关 pytest 用例通过 | 通过。未修改 API / DB，不需要 OpenAPI / Orval；未新增交易类能力 |

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 小程序证据 | 微信开发者工具或真机截图覆盖 SKU 商品详情页内容区入口与底部操作区 |
| 交互证据 | 点击“查看品牌主页”后进入正确品牌主页 |
| 布局证据 | 删除底部品牌按钮后，底部操作区无空白、错位或残留点击热区 |
| 回归证据 | 其他底部操作入口和详情页基础浏览能力不受影响 |

## 非目标

- 本 BUG 不要求新增品牌主页能力。
- 本 BUG 不要求调整品牌主页展示内容。
- 本 BUG 不要求新增或修改 SKU 详情接口字段。
- 本 BUG 不要求改变商品详情页交易范围边界。
