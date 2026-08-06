---
bug_id: BUG-0121-stale-scan-pending-business-word
review_status: approved
created_at: 2026-08-06 11:50:49
updated_at: 2026-08-06 11:50:49
reviewed_at: 2026-08-06 11:50:49
reviewer: AI
---

# 评审结论

确认修复，评审结论已通过，后续已交付闭环。

# 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 探索阶段已用临时 Sprint/Issue 夹具复现：普通正文中的英文 P 词示例曾命中 `issue-subdocument-stale-state` blocker。 |
| 严重等级合理 | 通过 | `medium` 合理；该问题不影响线上业务数据，但会误阻断 Sprint archive readiness 并干扰 Issue 写作规范。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖业务正文放行、结构化状态字段阻断、流程说明阻断和 readiness gate 一致性。 |
| 是否需 hotfix 路径 | 不需要 | 属于治理脚本误报，建议进入常规 Sprint 修复；如近期 Sprint archive 被阻断，可优先纳入当前治理 Sprint。 |

# 门禁结论

- 可进入 `/sprint-propose`。
- 纳入 Sprint 后可执行 `/bug-opsx` 创建修复 Change。
- 修复时不得直接绕过 stale scan；应通过上下文识别和回归测试保留真实中间态阻断能力。
