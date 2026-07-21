---
requirement_id: REQ-0054-brand-card-common-component
title: 微信小程序品牌卡片组件 prototype context
status: pending_review
created_at: 2026-07-19 17:45:31
updated_at: 2026-07-19 17:45:31
owner: product
source: acceptance.md
---

# 微信小程序品牌卡片组件 prototype context

## 1. 目标

该 prototype 用于描述微信小程序品牌卡片组件的视觉层级、状态和验收重点。首版服务 SKU 详情页品牌入口，后续可复用于品牌商品列表、同品牌推荐和首页品牌推荐。

## 2. 信息结构

```text
brand-card
├── brand-logo：品牌 Logo / 首字占位 / 默认占位
├── brand-copy
│   ├── brand-name：品牌名称
│   └── brand-hint：入口提示或副文案
└── brand-arrow：进入品牌内容提示
```

## 3. 状态

| 状态 | 说明 | 验收重点 |
|---|---|---|
| normal | 有 Logo、品牌名称和入口 | 信息完整、点击进入品牌入口 |
| logo-fallback | Logo 缺失或加载失败 | 展示首字/占位，不破图，不跳高 |
| long-name | 品牌名称较长 | 小屏不溢出、不遮挡箭头 |
| unavailable | 品牌入口不可用 | 展示禁用提示，阻止无效跳转 |

## 4. 移动端验收

- 320/375/430 pt 宽度截图检查卡片内容不重叠。
- Logo 容器固定尺寸，加载前后高度稳定。
- 点击热区覆盖整张卡片，触控高度不小于 44px。
- 卡片外边距与 SKU 详情页 summary/panel 视觉节奏一致。
- 无 Logo、长品牌名、无入口三类状态必须单独截图。

## 5. 后续实现提示

- 小程序实现时建议放入 `src/miniapp/components/brand-card/`。
- SKU 详情页只负责传入 `product.brand`、`skuId` 和来源上下文。
- 组件不直接请求接口，不承接品牌商品列表分页、筛选、加载态。
- 跳转 fallback 到搜索页时必须编码品牌名称。

