---
requirement_id: REQ-0065-sku-metadata-name-sku-dedup
title: SKU 元数据名称与编码展示去重原型上下文
status: approved
created_at: 2026-07-21 17:50:00
updated_at: 2026-07-21 17:57:47
---

# 原型上下文

## 目的

本原型用于固定管理端 SKU 列表与新增/编辑弹窗的字段语义，避免“SKU 名称”和“SKU 编码”在用户视角重复出现。

## 关键决策

- 商品名称：运营填写，对外展示，作为管理端和公开端主标题。
- SKU 编码：系统自动生成，唯一、稳定，用于内部识别、搜索和排障。
- 小程序/店主端：只展示商品名称，暂不展示 SKU 编码。

## 管理端列表目标状态

- 第一列主标题展示商品名称。
- SKU 编码可展示为弱化内部编号，也可在详情/hover/内部区呈现；不得抢占主标题层级。
- 搜索 placeholder 使用“商品名称 / SKU 编码”，表达可搜但不要求手填。

## 管理端弹窗目标状态

- 字段 label 使用“商品名称”。
- SKU 编码由系统自动生成；弹窗可展示只读提示“保存后系统自动生成”，不得要求运营输入。
- 保持现有 SKU 宽弹窗布局和滚动策略。

## 小程序/店主端目标状态

- 商品卡片、SKU 详情标题、参数区、推荐卡片、收藏列表和分享标题不展示 SKU 编码。
- 分享标题使用品牌名称 + 商品名称。

## Prototype 资产

```text
prototype/web/
├── sku-metadata-name-sku-dedup.html
└── sku-metadata-name-sku-dedup-context.md
```

PNG Golden Reference 可在后续 OpenSpec Change 或实现阶段按需导出，不阻塞本需求评审。
