---
title: 需求捕获
purpose: REQ-0006 瓷砖SKU管理页面轻量记录
content: 补录 capture（原目录仅有 requirement.md 与 prototype）
source: 基于 requirement.md v4 回溯
update_method: PRD 重大变更时同步
owner: product
status: captured
note: /req-complete 补录
---

# 需求捕获

## 一句话

管理后台提供瓷砖 SKU 列表、筛选、新增/编辑弹窗，支持多图主图、多视频、参考价格与草稿默认状态。

## 来源

- 管理后台首页框架（REQ-0004-admin-home）
- ui-design.md 暗色旗舰风
- v4 原型：`tile-sku-management-list.html`、`tile-sku-create-modal.html`

## 优先级

P0 — 核心商品主数据能力

## 范围边界

**本期**：列表页 + 新增/编辑弹窗 + 图片/视频上传 + 上下架 + 条件删除  
**非本期**：批量导入导出、SKU 复制、前台店主端展示页、价格策略引擎
