---
bug_id: BUG-0077-miniapp-category-secondary-name-truncated
status: done
review_result: approved
reviewed_at: 2026-07-21 15:00:29
reviewer: AI
created_at: 2026-07-21 15:00:29
updated_at: 2026-07-22 09:15:11
related_requirement: REQ-0045-category-list-page
related_change: fix-miniapp-category-secondary-name-truncated
---

# Review - BUG-0077 微信小程序分类页二级分类名称超过 4 个字被省略

## 评审结论

确认修复，状态批准为 `approved`。

该缺陷属于微信小程序分类页已交付能力中的长文本展示适配问题。二级分类名称超过 4 个字时被省略为 `...`，会影响用户识别分类含义和选择对应商品列表入口。缺陷边界清晰，严重等级合理，回归验收已覆盖长名称展示、布局稳定和分类点击正确性，可进入后续 `/bug-opsx` 和 Sprint 规划流程。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户反馈明确；根因初步指向二级分类文本区域固定宽度、单行截断或长文本适配不足 |
| 严重等级合理 | 通过 | `medium` 合理；问题不阻断页面打开，但影响分类页核心浏览体验 |
| 回归验收明确 | 通过 | acceptance.md 已覆盖 4 字以内、5-8 字、超过 8 字名称、布局稳定、点击入口和多端回归 |
| 是否需 hotfix 路径 | 不需要 | 当前无数据安全、接口不可用或全量阻断证据，无需 hotfix |

## 修复前置说明

- 可进入 `/bug-opsx BUG-0077-miniapp-category-secondary-name-truncated` 创建修复 Change。
- 可纳入后续 Sprint 正式范围。
- 修复应保持 `REQ-0045` 分类列表页范围边界，不新增分类管理、商品排序、购物车、交易或营销能力。
- 若仅调整小程序分类页前端样式且 API 契约不变，不需要 OpenAPI / Orval。
- 若实际修改分类 API 字段或响应结构，必须同步 OpenAPI、Orval、接口文档和测试。

## 评审记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-21 15:00:29 | /bug-review --approve | approved |
