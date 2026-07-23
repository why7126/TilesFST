---
bug_id: BUG-0079-admin-dashboard-overview-mock-data
title: 管理端首页数据概览仍使用 Mock 数据
status: done
severity: medium
review_result: approved
reviewed_at: 2026-07-22 08:28:57
approved_at: 2026-07-22 08:28:57
created_at: 2026-07-22 08:28:57
updated_at: 2026-07-22 09:27:20
reviewer: AI
source_command: /bug-review --approve
---

# 评审结论

批准修复。

# 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户反馈明确指出管理端首页数据概览仍使用 Mock 数据，root-cause 已给出数据源接入遗漏的推断根因和后续定位方向 |
| 严重等级合理 | 通过 | `medium` 合理；该问题影响管理端首页信息可信度，但当前未发现阻断、权限绕过或数据写入风险 |
| 回归验收明确 | 通过 | acceptance 已覆盖真实数据源、统计口径、数据变更、loading/empty/error、权限边界和自动化回归 |
| 是否需 hotfix 路径 | 不需要 | 当前未确认生产关键经营指标全面失真或阻断核心操作，按常规 BUG 修复流程推进 |

# 评审说明

该缺陷属于已交付管理端首页能力与真实业务数据接入预期不一致。修复前应先定位首页概览的 Mock 数据来源，并确认是否需要新增或复用后端统计接口。若后续实现涉及新增 API，需要同步 OpenAPI、Orval、API 文档和测试。

# 后续动作

1. 已创建 OpenSpec Change：`fix-admin-dashboard-overview-real-data`。
2. 可通过 `/sprint-propose` 纳入 Sprint 正式范围。
3. 实现前需确认真实统计口径和权限边界。
