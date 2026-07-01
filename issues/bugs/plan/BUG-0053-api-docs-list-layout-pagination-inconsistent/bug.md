---
bug_id: BUG-0053-api-docs-list-layout-pagination-inconsistent
title: 接口文档列表冗余系统接口信息且分页未与 SKU 页一致
severity: medium
status: draft
owner: product
discovered_at: 2026-07-01 09:09:32
environment: local
related_requirement: REQ-0022-admin-api-docs-menu
related_change: null
created_at: 2026-07-01 09:24:26
updated_at: 2026-07-01 09:24:26
---

# 缺陷说明

## 现象

Web 管理端 `/admin/api-docs` 接口文档列表区域存在不符合预期的「系统接口」信息，并且接口列表底部分页交互与瓷砖 SKU 管理页不一致。

当前静态探索结果显示：

- `/admin/api-docs` 的接口列表区固定渲染标题「系统接口」。
- 接口列表底部仅展示「共 x 个接口」与「当前筛选 x 条」，未提供上一页、当前页、下一页与每页显示条数选择。
- 瓷砖 SKU 管理页底部分页已提供 `page-summary`、`page-right`、页码按钮与每页条数选择，是本 BUG 期望对齐的基准。

> 待确认：用户反馈中的「第一行【系统接口】信息」当前在代码中更像是列表区标题，而不是某条接口数据行。后续 `/bug-complete` 或修复前需要确认是移除标题、改名，还是过滤某类真实数据行。

## 复现步骤

1. 使用管理员账号登录 Web 管理端。
2. 打开 `/admin/api-docs` 接口文档页。
3. 查看接口列表区域顶部是否出现「系统接口」信息。
4. 查看接口列表底部是否存在与 `/admin/tile-skus` 一致的分页控件。
5. 对照 SKU 页分页：左侧总数，右侧上一页、当前页、下一页与每页显示条数选择。

## 期望结果

- 接口文档列表不展示冗余的「系统接口」首行/标题信息，列表信息层级与管理端其他列表页一致。
- 接口列表提供分页能力与分页 UI。
- 分页交互和视觉结构与瓷砖 SKU 页保持一致，包括左侧统计文案、右侧页码按钮和每页条数选择。
- 筛选条件变化后分页应回到第一页，分页总数应基于当前筛选结果计算。

## 实际结果

- 接口列表区域存在「系统接口」信息，容易被理解为冗余首行或多余标题。
- 接口列表没有真实分页控件。
- 底部仅显示统计文本，无法切换页码或每页条数。
- 当前实现与 REQ-0022 横切验收中“分页 DOM 对齐管理端列表页”的要求不一致。

## 影响范围

- 影响端：Web 管理端。
- 影响页面：`/admin/api-docs`。
- 不影响店主 Web 展示端。
- 不影响微信小程序。
- 当前判断不涉及后端接口契约、数据库结构、MinIO 或媒体上传。
- 当前判断不需要重新生成 Orval，除非后续修复选择改造后端接口返回分页结构。

## 严重等级说明

严重等级为 `medium`。

理由：

- 该问题不阻断管理员进入接口文档页，也不影响权限控制或接口数据安全。
- 该问题影响管理端列表页一致性、接口目录可读性与分页操作体验。
- 关联 `REQ-0022-admin-api-docs-menu` 已进入 Sprint 且对应 Change 已 apply，属于已交付能力的验收偏差。

## 关联信息

- 关联需求：`REQ-0022-admin-api-docs-menu`
- 预期修复 Change：`fix-api-docs-list-layout-pagination-inconsistent`
- 参考页面：`/admin/tile-skus`
- 参考文件：
  - `src/web/src/pages/admin/ApiDocsPage.tsx`
  - `src/web/src/pages/admin/TileSkuManagementPage.tsx`
  - `issues/requirements/review/REQ-0022-admin-api-docs-menu/acceptance.md`
