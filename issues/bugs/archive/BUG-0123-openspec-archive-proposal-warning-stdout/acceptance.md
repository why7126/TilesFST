---
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
acceptance_status: passed
created_at: 2026-08-06 13:18:13
updated_at: 2026-08-06 17:17:37
---

# Acceptance

## 回归验收项

| 编号 | 验收项 | 预期 |
|---|---|---|
| AC-001 | 中文优先 Change 归档成功路径过滤已知 proposal scaffold warning | 执行归档 wrapper 后，成功输出不展示已知 proposal warning 块。 |
| AC-002 | 未知 stdout 保留 | OpenSpec CLI 输出未知 stdout 时，wrapper 不应静默吞掉，用户仍能看到诊断内容。 |
| AC-003 | 未知 stderr 保留 | OpenSpec CLI 输出未知 stderr 时，wrapper 不应静默吞掉，用户仍能看到诊断内容。 |
| AC-004 | BUG-0119 不回归 | 自定义固定说明噪音仍不出现在归档成功输出中。 |
| AC-005 | 失败路径诊断不丢失 | OpenSpec CLI 归档失败时，wrapper 仍输出必要错误信息并返回非零退出码。 |

## 建议验证命令

```bash
python -m pytest tests/test_archive_change_output.py
```

如现有测试文件命名不同，可在实现阶段将上述验收映射到 `scripts/archive-change.sh` 相关测试。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: fix-openspec-archive-proposal-warning-stdout
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

