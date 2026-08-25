---
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
created_at: 2026-08-22 14:27:46
updated_at: 2026-08-22 14:27:46
---

# User Stories

## US-001 产品负责人查看 linked Change 当前状态

作为产品负责人，我希望打开 REQ/BUG 主文档或 registry 当前态时能直接看到 linked Change，以便不用在 `trace.md`、Sprint scope 和 OpenSpec Change 之间来回反查。

验收要点：

- REQ 执行 `req.opsx` 后，`requirement.md` 可读入口展示当前 linked Change。
- BUG 执行 `bug.opsx` 后，`bug.md` 可读入口展示当前 linked Change。
- registry 当前态行与 trace 中的 linked Change 不冲突。

## US-002 AI Agent 使用原始 Issue ID 执行后续命令

作为 AI Agent，我希望 `/opsx-apply <REQ-id|BUG-id>` 和 `/opsx-archive <REQ-id|BUG-id>` 能稳定从 Issue 解析到真实 Change，以便遵守“后续命令参数使用原始 Issue ID”的流程契约。

验收要点：

- `trace.md.openspec_changes[]` 包含当前 active linked Change。
- 主文档和 registry 的 `related_change` 与当前 linked Change 一致。
- 已纳入 Sprint 的 Issue 创建 Change 后，`--sprint auto` 能解析到同一 Sprint。

## US-003 流程维护者集中维护 linked Change 回填

作为流程维护者，我希望 linked Change 的回填逻辑集中在 Workflow Sync 或共享脚本中，以便避免 `/req-opsx`、`/bug-opsx`、Sprint 同步和 registry 更新各自手工补写。

验收要点：

- `req.opsx` 和 `bug.opsx` 使用同一套或对称的同步逻辑。
- 重复运行 Workflow Sync 不产生重复条目。
- 同步摘要能说明 trace、主文档、registry 和 Sprint scope 的更新或跳过情况。

## US-004 评审者发现 linked Change 漂移

作为评审者，我希望 focused dry-run 或测试能发现 trace、主文档、registry、Sprint scope 之间的 linked Change 漂移，以便在进入 apply 或 archive 前修复。

验收要点：

- 当 `requirement.md` 或 `bug.md` 缺失 linked Change 时，检查能报告漂移。
- 当 registry 的 `related_change` 滞后时，检查能报告差异。
- 当 Sprint scope 缺少 Change 时，后续 apply dry-run 不会被误判为可执行。

## US-005 Sprint 负责人确认 scope 自动补齐

作为 Sprint 负责人，我希望已纳入 Sprint 的 REQ/BUG 在创建 Change 后自动补齐 `sprint.yaml` 的 `changes[]` 和 `scope_estimates[].change`，以便 Sprint 四件套与 Issue linked Change 一致。

验收要点：

- `req.opsx` 后 REQ 所属 Sprint 包含新 Change。
- `bug.opsx` 后 BUG 所属 Sprint 包含新 Change。
- open-change 延后项被清理或不再继续提示已完成的 opsx 步骤。
