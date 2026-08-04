---
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
status: pending_review
created_at: 2026-08-04 08:35:48
updated_at: 2026-08-04 08:35:48
owner: product
source: acceptance.md
---

# Prototype Context

## 目的

本 prototype 表达管理端列表字段展示 adapter 检查表的工作台形态，用于后续 OpenSpec design 参考。它不是最终产品页面承诺，也不要求本阶段修改管理端源码。

## 覆盖

- 首批列表：品牌、证书、SKU、Banner。
- 三类 adapter：image、name、fallback。
- 检查状态：必选、推荐、N/A、待治理。
- 横切门禁：分页 DOM、fixed toast、DS confirm、禁止 `window.confirm`。

## 视觉约束

- 遵守管理端暗色旗舰风。
- 使用语义化颜色变量表达页面底色、文字、边框和品牌金。
- 信息密度偏工作台，不做营销式 hero。
- 表格/清单布局应稳定、可扫描，避免卡片嵌套。

## 待导出

- PNG Golden Reference：待 OpenSpec design 阶段按最终页面落点决定是否导出。
