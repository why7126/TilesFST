---
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
status: done
created_at: 2026-08-06 14:02:15
updated_at: 2026-08-06 15:08:58
severity_hint: medium
environment: local
related_requirement:
related_bug: BUG-0123-openspec-archive-proposal-warning-stdout
captured_via: capture
classification_rationale: 已归档修复仍未覆盖真实 OpenSpec CLI 多行 proposal warning stdout 块，属于已交付修复范围内的行为偏差。
---

# 现象

`fix-openspec-archive-proposal-warning-stdout` 已归档后，真实归档成功输出中仍展示 OpenSpec CLI 的多行 proposal warning 块：

```text
Proposal warnings in proposal.md ...
Missing required sections ...
```

当前修复似乎只覆盖了单行 warning 或固定形态，未整体吸收 CLI stdout 中的多行 warning 块。

# 复现步骤

1. 准备或复用会触发 OpenSpec CLI proposal warning 的 Change。
2. 执行 `scripts/archive-change.sh <change-id>`，或通过 `/opsx-archive` 间接触发归档。
3. 观察归档成功路径输出中的 stdout 内容。

# 期望 vs 实际

期望：真实 OpenSpec CLI 多行 proposal warning 块应被整体吸收，归档成功输出不再展示该已知噪音；未知 stdout/stderr 仍保留，避免吞掉真实异常或诊断信息。

实际：归档成功输出仍展示多行 proposal warning 块，影响 `/opsx-archive` 验收体验。

# 附件

暂无。
