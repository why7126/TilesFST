---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式与瓷砖 SKU 页不一致 - 临时规避
severity: medium
status: approved
owner: product
created_at: 2026-07-01 13:54:17
updated_at: 2026-07-01 14:01:11
related_requirement: REQ-0022-admin-api-docs-menu
---

# 临时规避方案

## 管理员操作规避

该缺陷仅影响 `/admin/api-docs` 摘要指标卡视觉一致性，不影响接口目录、筛选、Swagger 入口、OpenAPI JSON 入口或 Orval 方法名展示。

在修复前，管理员可继续使用接口文档页完成接口查询与文档跳转。

## 验收规避

在进行 REQ-0022 相关人工验收时，应将该缺陷作为已知 UI 偏差单独记录，不应把接口摘要指标卡视为已满足“与 SKU 页同类指标卡一致”的验收项。

若需要判断接口统计数据是否正确，可优先检查数值内容与接口列表行数据，而不是依赖指标卡视觉样式。

## 风险

该规避方案不能解决管理端页面一致性问题，也不能满足 Design System 对同类组件复用的预期。因此该 BUG 仍需进入后续修复流程。

## 禁止规避方式

- 不得通过放宽 `rules/ui-design.md` 来接受该偏差。
- 不得在接口文档页新增裸 Hex、页面私有视觉风格或一次性样式覆盖来“看起来接近”。
- 不得绕过 OpenSpec Change 直接修改生产页面。
