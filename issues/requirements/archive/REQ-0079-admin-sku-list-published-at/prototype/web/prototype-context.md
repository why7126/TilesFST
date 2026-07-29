---
requirement_id: REQ-0079-admin-sku-list-published-at
title: 管理端瓷砖 SKU 列表新增发布时间列 - 原型说明
status: pending_review
owner: product
created_at: 2026-07-28 22:46:01
updated_at: 2026-07-28 22:46:01
---

# 原型说明

## 1. 原型目标

本原型用于确认管理端瓷砖 SKU 列表新增“发布时间”列后的列顺序、时间格式和空值展示，不用于重设页面视觉风格。

## 2. 适用范围

- 终端：企业内部 Web 管理端。
- 页面：瓷砖 SKU 列表页。
- 变化：在“更新时间”列前新增“发布时间”列。
- 不包含：筛选项新增、排序新增、导出字段、发布流程、弹窗或上传。

## 3. 设计约束

- 继续复用管理端列表页模板或既有 SKU 列表 DOM。
- “发布时间”列与“更新时间”列视觉层级一致。
- 时间格式示例保持一致：`2026-07-28 10:18:35`。
- 无发布时间展示 `-`。
- 宽表按现有横向滚动策略处理，避免时间列挤压操作列。
- 实现时必须使用 Design System semantic token，不得新增裸 Hex。

## 4. 验收关注点

- 列顺序：发布时间在更新时间之前。
- 语义：发布时间与更新时间不是同一字段。
- 兼容：无发布时间不会渲染异常。
- 横切：分页 DOM、fixed toast 和 `window.confirm` gate 仍按 admin-list best-practice 验收。

## 5. PNG

PNG Golden Reference 待后续设计确认后导出；当前以 HTML 原型和本 context 作为设计策略来源。
