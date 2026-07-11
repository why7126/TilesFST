---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
title: 归档后 issue 子文档状态一致性检查缺失临时规避方案
status: archived
severity: high
owner: product
created_at: 2026-07-11 16:05:13
updated_at: 2026-07-11 20:13:04
related_requirement:
related_change:
---

# 临时规避方案

## 当前可用规避

在正式修复前，执行 `/opsx-archive` 或 `/sprint-archive` 前后，人工增加一次聚焦检查：

```bash
rg -n "^\\s*status:\\s*(draft|pending_review|in_sprint|applied|todo|open)\\b" \
  issues/requirements/archive issues/bugs/archive \
  --glob "*.md"
```

若只检查即将归档的单个 issue 包，可将搜索范围缩小到对应目录：

```bash
rg -n "^\\s*status:\\s*(draft|pending_review|in_sprint|applied|todo|open)\\b" \
  issues/bugs/archive/BUG-xxxx-slug \
  --glob "*.md"
```

## 处理建议

- 对真实已闭环的子文档，将状态同步为符合归档语义的状态，例如 `done`。
- 对仍需人工复核的子文档，不应继续归档；应先补齐评审或验收。
- 对历史 archive 包的大批量残留状态，不建议在没有上下文复核时机械替换，应按 Sprint、REQ 或 BUG 分批清理。

## 注意事项

- 不要直接编辑 `sprint.md` 的 workflow-sync marker block。
- 不要通过删除子文档来规避状态残留。
- 不要把未完成的 `pending_review` 文档改成 `done` 来绕过归档门禁；应先确认验收或评审事实。
- 对已经归档的历史包，应优先生成清单，再由对应负责人判断是否批量修正。

## 不可规避场景

- 只依赖当前 `/opsx-archive` 或 `/sprint-archive` 默认流程，无法自动发现该类残留。
- 只运行 `scripts/validate-sprint-archive-readiness.py`，当前也无法发现 issue 子文档状态残留。
