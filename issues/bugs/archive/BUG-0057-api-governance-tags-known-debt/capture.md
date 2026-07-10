---
bug_id: BUG-0057-api-governance-tags-known-debt
status: captured
created_at: 2026-07-04 15:25:45
updated_at: 2026-07-04 15:25:45
severity_hint: medium
environment: local
related_requirement:
related_bug:
---

# 现象

API governance 中标记为 `known-debt` 的既有 route tags 清理失败，导致 API 治理标签仍保留历史债务状态，无法完成预期的 tags 收敛。

# 复现步骤

1. 执行或检查 API governance 的 route tags 清理流程。
2. 观察既有 route tags 中标记为 `known-debt` 的条目。
3. 确认清理动作未能移除、替换或规范化这些历史 tags。

# 期望 vs 实际

- 期望：API governance 可识别并清理既有 route tags 的 `known-debt` 标记，使 OpenAPI tags 与治理规范保持一致。
- 实际：清理失败，`known-debt` 标记仍残留在 API route tags 中。

# 附件

待补充：失败命令输出、OpenAPI tags 截图或相关 route 文件路径。
