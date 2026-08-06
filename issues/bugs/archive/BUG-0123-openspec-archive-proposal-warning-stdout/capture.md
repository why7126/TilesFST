---
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
status: done
created_at: 2026-08-06 12:10:56
updated_at: 2026-08-06 13:57:20
severity_hint: medium
environment: local
related_requirement:
related_bug: BUG-0119-openspec-archive-scaffold-warning-noise
captured_via: capture
classification_rationale: 既有 OpenSpec 归档 wrapper 成功路径仍暴露已知 warning 噪音，属于已交付修复范围内的行为偏差。
---

# 现象

`scripts/archive-change.sh` 在归档成功路径中仍会将 OpenSpec CLI stdout 中的 proposal warning 块展示给用户。此前 BUG-0119 已修复自定义固定说明噪音，但 wrapper 尚未吸收 CLI stdout 中的已知 proposal scaffold warning。

# 复现步骤

1. 准备一个中文优先的 OpenSpec Change，并使其满足归档条件。
2. 执行归档 wrapper，例如 `scripts/archive-change.sh <change-id>` 或通过 `/opsx-archive` 间接触发。
3. 观察成功输出中的 stdout 内容。

# 期望 vs 实际

期望：归档成功时，stdout 不展示已知 proposal scaffold warning；未知 stdout/stderr 仍保留，避免吞掉真正异常或诊断信息。

实际：归档 wrapper 仍未吸收 OpenSpec CLI stdout 中的 proposal warning 块，导致成功路径输出出现已知噪音，影响 `/opsx-archive` 验收体验。

# 附件

暂无。
