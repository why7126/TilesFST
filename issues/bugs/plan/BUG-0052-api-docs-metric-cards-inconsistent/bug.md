---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式与瓷砖 SKU 页不一致
severity: medium
status: draft
owner: product
discovered_at: 2026-07-01 09:09:32
environment: local
related_requirement: REQ-0022-admin-api-docs-menu
related_change: null
created_at: 2026-07-01 09:23:35
updated_at: 2026-07-01 09:23:35
---

# 缺陷说明

## 现象

Web 管理端 `/admin/api-docs` 页面标题下方的接口摘要指标卡，与瓷砖 SKU 管理页 `/admin/tile-skus` 的同类指标卡样式不一致。

当前接口文档页摘要区展示了接口总数、受保护接口数、Orval 映射数、非 `/api/v1` 路由数，但卡片内部文字层级、数字样式、说明文字间距与 SKU 页指标卡不一致，影响管理端页面一致性。

## 复现步骤

1. 使用管理员账号进入 Web 管理端。
2. 打开 `/admin/api-docs` 接口文档页。
3. 查看标题下方的四个接口摘要指标卡。
4. 打开 `/admin/tile-skus` 瓷砖 SKU 页。
5. 对照 SKU 页标题下方的四个 SKU 统计指标卡。

## 期望结果

- `/admin/api-docs` 的指标卡应复用或对齐瓷砖 SKU 页同类指标卡结构与样式。
- 指标卡应保持一致的布局、边框、圆角、间距、文字层级、数字强调色与说明文字弱化层级。
- 实现应继续使用管理端 Design System semantic token，不新增裸 Hex。

## 实际结果

- `/admin/api-docs` 指标卡与 `/admin/tile-skus` 指标卡视觉不一致。
- 接口文档页指标卡内部结构未使用 SKU 页同类指标卡的 `.metric-value` 与 `.metric-desc` 层级，导致全局指标卡样式不能完整命中。

## 影响范围

- 影响端：Web 管理端。
- 影响页面：`/admin/api-docs`。
- 不影响店主 Web 展示端。
- 不影响微信小程序。
- 不影响后端 API 行为、数据库结构、MinIO 或媒体上传链路。
- 影响 Design System 一致性验收，以及 REQ-0022 的管理端列表/页面一致性质量门禁。

## 严重等级说明

严重等级为 `medium`。

理由：该缺陷不阻断接口文档页核心功能，不影响权限、接口数据、Swagger 策略或 Orval 映射展示；但属于已交付管理端页面的 UI 一致性偏差，影响 Design System 验收与管理端体验一致性，应进入常规 fix 流程修复。
