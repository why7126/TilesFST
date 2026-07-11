---
bug_id: BUG-0063-archived-change-trace-fallback-summary
title: archived Change 缺失 trace.md 时归档验证摘要兜底检查缺失临时规避
status: archived
created_at: 2026-07-11 16:06:00
updated_at: 2026-07-11 20:13:04
---

# 临时规避方案

在正式修复前，执行 `/opsx-archive` 或 `/sprint-archive` 时不要只依赖 `validate-sprint-archive-readiness.py` 的 `PASS` 结论。

临时检查方式：

1. 对待归档或已归档 Change 检查 `trace.md` 是否存在。
2. 若 `trace.md` 缺失，人工检查 `proposal.md`、`design.md`、`tasks.md` 是否至少包含以下信息：
   - 验证命令与结果。
   - 验收结论。
   - 归档路径或归档时间。
   - 关联 Issue / Sprint 状态同步说明。
3. 若上述信息缺失，归档前补充 `trace.md` 或补充标准化归档验证摘要。

# 风险与限制

- 人工检查容易遗漏，无法替代自动化门禁。
- 不同 Change 的摘要格式不统一，复盘和审计仍需人工拼接证据。
- 历史 archived Change 可能已经缺失 trace，需要修复脚本支持对历史包输出 warning 或 blocker。

# 是否可不修

不建议长期不修。

理由：该问题不影响业务运行，但会削弱 OpenSpec archive 作为事实源的可信度，并让 Sprint 复盘、Fact Sheet、workflow-sync 审计依赖分散文档推断。
