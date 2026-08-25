---
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
acceptance_status: passed
created_at: 2026-08-22 14:27:46
updated_at: 2026-08-25 14:51:36
source_change:
source_sprint:
---

# Acceptance

## 功能 AC

- [ ] AC-001 `req.opsx` 创建或确认 Change 后，目标 REQ `trace.md` frontmatter 的 `openspec_changes[]` 包含当前 `change_id`，且重复运行不重复追加。
- [ ] AC-002 `req.opsx` 后，目标 REQ `trace.md` fenced yaml 状态块的 `openspec_changes[]` 与 frontmatter 不冲突。
- [ ] AC-003 `req.opsx` 后，目标 `requirement.md` frontmatter 或状态块展示当前 linked Change。
- [ ] AC-004 `req.opsx` 后，`issues/requirements/_registry.yaml` 对应条目的 `related_change` 更新为当前 linked Change。
- [ ] AC-005 `bug.opsx` 创建或确认 Change 后，目标 BUG `trace.md` frontmatter 与 fenced yaml 状态块均包含当前 `change_id`。
- [ ] AC-006 `bug.opsx` 后，目标 `bug.md` frontmatter 或状态块展示当前 linked Change。
- [ ] AC-007 `bug.opsx` 后，`issues/bugs/_registry.yaml` 对应条目的 `related_change` 更新为当前 linked Change。
- [ ] AC-008 如果 BUG 关联父 REQ，父 REQ `trace.md` 的 `## 关联缺陷` 索引显示最新 BUG 关联 Change。
- [ ] AC-009 已纳入 Sprint 的 REQ 执行 `req.opsx` 后，同一 Sprint 的 `sprint.yaml changes[]` 包含新 Change。
- [ ] AC-010 已纳入 Sprint 的 BUG 执行 `bug.opsx` 后，同一 Sprint 的 `sprint.yaml changes[]` 包含新 Change。
- [ ] AC-011 已纳入 Sprint 的 Issue 创建 Change 后，匹配的 `scope_estimates[].change` 自动填充或更新为该 Change。
- [ ] AC-012 已解决的 open-change 延后项不再继续提示已经完成的 `/req-opsx` 或 `/bug-opsx`。
- [ ] AC-013 Issue 未纳入 Sprint 时，Workflow Sync 可跳过 Sprint scope，但仍同步 trace、主文档与 registry，并在摘要说明 skipped 原因。
- [ ] AC-014 重复运行 `sync-workflow-status.py --event req.opsx|bug.opsx` 不产生重复 `openspec_changes`、`related_changes`、`related_change` 或无意义 diff。
- [ ] AC-015 focused dry-run 能报告 trace、主文档、registry 或 Sprint scope 的 linked Change 漂移，报告包含 Issue、Change、文件路径、当前值与期望值。
- [ ] AC-016 多 Change Issue 的主 linked Change 选择策略在设计或实现说明中明确，不允许静默覆盖人工无法判断的字段。
- [ ] AC-017 Workflow Sync 成功摘要包含 focused issue、focused change、subdocuments checked/updated、sprint sync 或 skipped 信息。
- [ ] AC-018 增加或更新测试覆盖 REQ 与 BUG 两条 opsx 链路的 trace、主文档、registry、Sprint scope 和幂等性。
- [ ] AC-019 后续 `/opsx-apply --sprint auto --change <change-id> --dry-run` 或等价门禁不再因 linked Change 未回填而报告 `change <id> not in sprint scope`。
- [ ] AC-020 同步和测试不得输出真实客户数据、密钥、`.env`、Authorization header、Cookie、本机绝对路径或原始 Codex session 内容。

## 横切 AC（knowledge-base）

无横切 AC：本需求为 Workflow Sync 与 opsx 链路治理，不涉及管理端列表、表单、弹窗或媒体上传 UI 场景。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 14:57:42
accepted_by: workflow-sync
source_change: update-workflow-opsx-linked-change-backfill
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

