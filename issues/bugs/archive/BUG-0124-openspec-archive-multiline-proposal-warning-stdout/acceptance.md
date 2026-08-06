---
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
acceptance_status: passed
created_at: 2026-08-06 14:30:16
updated_at: 2026-08-06 17:17:37
---

# Acceptance

## 回归验收项

| 编号 | 验收项 | 预期 |
|---|---|---|
| AC-001 | 多行 proposal warning 块整体吸收 | OpenSpec CLI stdout 中出现 `Proposal warnings in proposal.md` 及后续 `Missing required sections` 等详情行时，归档成功输出不展示整个已知 warning 块。 |
| AC-002 | 未知 stdout 保留 | stdout 中出现不属于已知 proposal warning 块的内容时，归档 wrapper 仍展示该内容。 |
| AC-003 | 未知 stderr 保留 | stderr 中出现不属于已知 proposal warning 块的内容时，归档 wrapper 仍展示该内容。 |
| AC-004 | 单行 warning 回归不失效 | 既有单行 proposal warning 或固定提示过滤测试继续通过。 |
| AC-005 | BUG-0123/BUG-0119 不回归 | 已修复的 proposal warning stdout 噪音和自定义固定说明噪音不再回到成功路径输出。 |
| AC-006 | 失败路径诊断不丢失 | OpenSpec CLI 归档失败时，wrapper 仍输出必要错误信息并返回非零退出码。 |

## 建议验证命令

```bash
python -m pytest tests/test_archive_change_script.py
```

如现有测试文件命名不同，实现阶段应将上述验收映射到 `scripts/archive-change.sh` 相关测试，并至少新增一个真实多行 stdout warning 样例。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: fix-openspec-archive-multiline-proposal-warning-stdout
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

