# Change: fix-sprint-archive-incomplete-tasks-gate

## Why

BUG-0056 暴露出 `/sprint-archive` 的质量门禁只停留在文档描述层：Sprint 内 change 的 `tasks.md` 尚有未完成项时，仍可能被归档并关闭 Sprint。该问题已在 sprint-004 历史归档中出现，破坏 OpenSpec/Sprint 的完成状态可信度。

## What Changes

- 新增 Sprint 归档前置校验脚本，按 `sprint.yaml` 范围检查 active 与 archived change 的 `tasks.md` 完成度。
- 默认模式下，一旦发现未完成 task、缺失 `tasks.md` 或缺失 change 目录，脚本返回非零退出码。
- 更新 `/sprint-archive` Cursor 命令与 Codex skill，要求归档前、关闭 Sprint 前运行该校验。
- 增加 pytest 回归，覆盖完成通过、active 未完成阻断、archived 未完成阻断、缺失 `tasks.md` 阻断。

## Impact

- 影响流程脚本：`scripts/validate-sprint-archive-readiness.py`
- 影响流程文档：`.cursor/commands/sprint-archive.md`、`.agents/skills/source-command-sprint-archive/SKILL.md`
- 影响测试：`tests/test_sprint_archive_readiness.py`
- 不影响业务 API、数据库、Web UI、小程序、Docker Compose。

## Rollback Plan

如脚本误判，可临时在 `/sprint-archive` 中使用 `--force` 并保留人工确认记录；回滚时删除新增脚本与测试，并恢复命令文档，但不建议移除该门禁。
