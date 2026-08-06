---
bug_id: BUG-0122-archive-sync-issue-subdoc-residual-cleanup
created_at: 2026-08-06 11:41:58
updated_at: 2026-08-06 11:41:58
---

# 临时规避

在归档 promote 被 Issue 子文档状态门禁阻断时，先按报告定位目标 Issue，并执行 residual reconcile 的 dry-run 与 apply 流程。

示例：

```bash
python scripts/sync-workflow-status.py \
  --event req.archive \
  --req REQ-xxxx-slug \
  --sprint auto \
  --reconcile-issue-status-residuals \
  --dry-run
```

确认 dry-run 只包含可安全同步字段后，再执行：

```bash
python scripts/sync-workflow-status.py \
  --event req.archive \
  --req REQ-xxxx-slug \
  --sprint auto \
  --reconcile-issue-status-residuals \
  --apply-reconcile
```

BUG 条目使用 `--event bug.archive --bug BUG-xxxx-slug`。

# 风险

- 必须先 dry-run，避免把仍未闭环或需要人工判断的状态误同步为闭环态。
- 该规避只解决状态残留，不替代 `/opsx-archive`、`/sprint-archive` 或验收结论。
