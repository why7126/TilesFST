---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
status: archived
created_at: 2026-07-11 13:19:58
updated_at: 2026-07-11 20:13:04
severity_hint: high
environment: local
related_requirement:
related_bug:
---

# 现象

归档流程完成后，archive 包内的 issue 子文档仍可能残留非闭环状态，例如 `draft`、`pending_review`、`in_sprint`。当前归档校验缺少对子文档状态一致性的检查，导致已归档包表面完成，但内部文档状态仍表达“未完成/评审中/迭代中”。

# 复现步骤

1. 准备一个已进入归档流程的 REQ 或 BUG，其 issue 包内存在多个子文档（如 `capture.md`、`bug.md`、`trace.md`、`review.md`、`acceptance.md` 等）。
2. 让其中一个或多个子文档仍保留 `draft`、`pending_review` 或 `in_sprint` 等非归档闭环状态。
3. 执行 `/opsx-archive` 或 `/sprint-archive`，完成 Change / Sprint 归档。
4. 检查迁入 `issues/**/archive/` 的 issue 包内各子文档状态。

# 期望 vs 实际

- 期望：归档完成前或完成后必须校验 issue 包内所有维护状态的子文档；archive 包内不得残留 `draft`、`pending_review`、`in_sprint` 等非闭环状态。
- 实际：当前归档流程只同步主 trace/registry 等关键状态，未覆盖 issue 子文档状态一致性，archive 包内可能残留过期状态。

# 附件

- 用户反馈：归档后发现 archive 包内残留 `draft` / `pending_review` / `in_sprint`。
