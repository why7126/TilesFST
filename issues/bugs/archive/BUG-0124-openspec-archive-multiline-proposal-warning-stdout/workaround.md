---
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
created_at: 2026-08-06 14:30:16
updated_at: 2026-08-06 14:30:16
---

# Workaround

## 临时规避

暂无稳定自动化规避方式。执行 `/opsx-archive` 或 `scripts/archive-change.sh <change-id>` 时，如果归档最终成功，且输出中仅出现已知的 `Proposal warnings in proposal.md` / `Missing required sections` 多行兼容性 warning，可人工忽略该 warning 块。

## 注意事项

- 不应为了消除该 warning 回填英文脚手架章节；项目 OpenSpec 文档仍应遵守中文优先规范。
- 不应粗暴丢弃全部 stdout/stderr；未知输出可能包含真实错误、诊断信息或上游 CLI 行为变化信号。
- 若成功输出中同时出现未知 stdout/stderr，应保留并单独判断，不应被本缺陷的临时规避策略一并忽略。

## 后续处理

通过后续 OpenSpec Change 修复 `scripts/archive-change.sh` 多行 warning 块过滤逻辑，并补充覆盖真实多行 stdout 样例的回归测试。
