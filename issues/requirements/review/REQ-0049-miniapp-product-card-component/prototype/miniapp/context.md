---
requirement_id: REQ-0049-miniapp-product-card-component
status: pending_review
created_at: 2026-07-19 12:36:55
updated_at: 2026-07-19 12:36:55
---

# 小程序原型说明

## 1. 原型范围

本原型仅表达微信小程序商品卡片组件的视觉结构和关键状态，不表达完整商品列表容器、筛选、排序、分页或接口行为。

## 2. 组件结构

```text
ProductCard
├── ProductImage
│   ├── image
│   └── fallback
├── ProductInfo
│   ├── brandName
│   ├── skuName
│   ├── specAndColor
│   └── price
└── StatusLine
    ├── skuCode
    └── optionalTag
```

## 3. 推荐状态

| 状态 | 表现 |
|---|---|
| 默认 | 深色卡片、固定比例商品图、品牌金价格、紧凑辅助信息 |
| 图片失败 | 图片区域展示深色纹理占位和“暂无图片” |
| 不可查看 | 卡片降低强调度，展示“暂不可查看”，点击不跳转 |
| 双列紧凑 | 图片比例稳定，名称最多两行，价格仍保持可扫描 |

## 4. 视觉约束

- 背景沿用小程序深色企业轻奢风。
- 品牌金仅用于价格、状态强调和轻量标签。
- 卡片圆角接近直角，避免过度圆润。
- 图片容器固定比例，避免列表加载时上下跳动。
- 文本优先级：品牌/标签 < SKU 名称 < 规格辅助 < 参考价格。

## 5. 待导出

- PNG Golden Reference：待 `/req-opsx` 或设计评审阶段根据 HTML 原型导出。
