---
change_id: fix-archive-sync-issue-subdoc-residual-cleanup
status: applied
created_at: 2026-08-06 11:52:40
updated_at: 2026-08-06 11:58:11
---

# 任务

- [x] 1. 梳理 `sync-workflow-status.py`、`promote-issues-for-archive.py` 与子文档 drift helper 的残留分类与写入边界。
- [x] 2. 在归档同步或 promote 前置流程中接入可安全 residual reconcile，确保仅闭环 Issue 的安全残留会自动同步。
- [x] 3. 保留未闭环、缺验收、缺证据或语义不明字段的 warning/blocker 输出，不自动写入。
- [x] 4. 补充 BUG 与 REQ 场景回归测试，覆盖 `capture.md status: captured` 安全残留、人工判断残留、dry-run、apply 和幂等。
- [x] 5. 运行 `python scripts/validate-openspec-language.py`、相关 pytest 与目录结构校验。
- [x] 6. 修复完成后按需在 `docs/knowledge-base/incidents/` 记录归档状态残留治理经验。

说明：本次修复已由 `BUG-0122`、Change 文档和回归测试承载经验，暂不新增 incident 文档。
