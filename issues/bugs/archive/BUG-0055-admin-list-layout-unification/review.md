---
bug_id: BUG-0055-admin-list-layout-unification
title: 管理端多列表页布局与筛选分页交互未统一评审
severity: medium
status: approved
owner: product
review_result: approved
reviewed_at: 2026-07-03 18:44:50
created_at: 2026-07-03 18:44:50
updated_at: 2026-07-03 18:44:50
related_requirement: null
related_change: fix-admin-list-layout-unification
---

# 缺陷评审

## 评审结论

`approved`：确认修复。

该缺陷属于 Web 管理端多个已交付或在研列表页的 UI/交互一致性偏差，影响页面扫描路径、筛选操作习惯、表格操作列可达性和分页效率。缺陷包已具备根因分析、临时规避和明确回归验收标准，应进入后续 `/bug-opsx` 创建 `fix-admin-list-layout-unification` 修复 Change。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 已确认 Banner 页模块顺序不一致，多页保留查询按钮，多数分页仅展示当前页，固定操作列未跨页面统一 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断访问和数据维护，不涉及权限或数据损坏，但横跨多个高频管理页面 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖页面范围、模块顺序、无查询按钮、重置按钮一致、固定操作列、最多 5 页码和权限/业务回归 |
| 是否需 hotfix 路径 | 不需要 | 影响范围为 Web 管理端 UI/交互一致性，不涉及安全、数据损坏、生产阻断或核心写入失败 |

## 产品确认

本次修复范围包括瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计和接口文档页面。

修复基线：

- 模块顺序：标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块。
- 筛选/搜索模块：以瓷砖 SKU 页为交互与样式基线，但所有页面均移除【查询】功能。
- 表格最后一列：以接口文档页固定浮动操作列为基线。
- 分页：最多展示 5 个可点击页码；只有 1 页时也保持统一分页结构。

## 后续动作

1. 执行 `/bug-opsx BUG-0055-admin-list-layout-unification`。
2. 创建 `fix-admin-list-layout-unification` OpenSpec Change。
3. 修复时优先沉淀或复用管理端列表页公共结构，避免继续按页面局部修复。
4. 补充前端 Vitest/Testing Library 回归，覆盖模块顺序、无查询按钮、固定操作列、最多 5 页码与筛选重置页码。
5. 当前判断不需要后端 API、数据库、MinIO、媒体上传、Orval 或 Docker Compose 变更；若后续实现选择调整接口分页结构，则必须重新评估 API 与 Orval 门禁。
