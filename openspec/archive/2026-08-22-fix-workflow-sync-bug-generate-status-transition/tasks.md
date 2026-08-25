---
change_id: fix-workflow-sync-bug-generate-status-transition
source_bug: BUG-0136-workflow-sync-bug-generate-captured-draft
sprint: sprint-025
created_at: 2026-08-22 21:36:45
updated_at: 2026-08-22 21:47:46
---

# 任务

- [x] 1. 定位 `scripts/sync-workflow-status.py` 与 `scripts/workflow_sync/` 中 generate 事件状态转换逻辑。
- [x] 2. 补齐 `bug.generate` 的主状态推进：`captured` 目标 BUG 在 `bug.md` 已存在时推进到 `draft`。
- [x] 3. 确保 trace frontmatter、fenced YAML、`lifecycle.generated`、registry、CHANGELOG 和 `bug.md` frontmatter 使用同一个目标状态。
- [x] 4. 增加缺少 `bug.md` 的保护逻辑，不误推进状态，并输出 warning 或 no-op 摘要。
- [x] 5. 增加聚焦回归测试，覆盖首次 `bug.generate`、重复 `bug.generate`、缺失 `bug.md` 和 REQ/BUG generate 对照。
- [x] 6. 运行聚焦测试与工作流校验：`pytest` 相关测试、`python scripts/validate-openspec-language.py`、`python scripts/validate-directory-structure.py`、Workflow Sync dry-run。
- [x] 7. 回填 BUG-0136 acceptance 与 Change trace 验收结果。
- [x] 8. 归档前评估是否需要沉淀 `docs/knowledge-base/incidents/`；如无长期复用价值，记录不适用原因。
