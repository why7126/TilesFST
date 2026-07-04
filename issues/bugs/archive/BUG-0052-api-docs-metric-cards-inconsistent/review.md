---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式与瓷砖 SKU 页不一致 - 评审记录
severity: medium
status: approved
owner: product
review_result: approved
reviewed_at: 2026-07-01 14:01:11
created_at: 2026-07-01 14:01:11
updated_at: 2026-07-01 14:01:11
related_requirement: REQ-0022-admin-api-docs-menu
---

# 评审记录

## 评审结论

`approved`，确认需要修复。

BUG-0052 已满足进入修复流程的条件：缺陷可稳定复现，根因分析充分，严重等级为 `medium` 合理，回归验收标准明确。该问题不需要 hotfix 路径，可进入常规 `fix-*` OpenSpec Change。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `/admin/api-docs` 摘要卡缺少 `.metric-value` / `.metric-desc`，与 `/admin/tile-skus` 基准结构不一致 |
| 严重等级合理 | 通过 | 不阻断接口文档功能，但影响管理端页面一致性与 Design System 验收，定级 `medium` |
| 回归验收明确 | 通过 | `acceptance.md` 覆盖 DOM 结构、视觉层级、semantic token、功能不回归、权限边界与前端测试 |
| 是否需 hotfix 路径 | 不需要 | 问题属于 UI 一致性偏差，不涉及安全、数据损坏、接口不可用或生产阻断 |

## 修复门禁

- 后续可执行 `/bug-opsx BUG-0052-api-docs-metric-cards-inconsistent`。
- 建议 Change 命名沿用 `fix-api-docs-metric-cards-inconsistent`。
- 修复时应优先最小化调整 `ApiDocsPage` 摘要卡 DOM 结构，复用管理端既有 metric class。
- 修复时必须补充或更新 `ApiDocsPage` 前端测试，覆盖 `.metric-value` 与 `.metric-desc`。
- 修复不应修改后端 API、数据库、MinIO、Orval 或 Docker Compose 配置。

## 评审备注

本次评审只确认缺陷是否进入修复流程，不修改 `src/`，不创建 OpenSpec Change。
