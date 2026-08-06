---
bug_id: BUG-0121-stale-scan-pending-business-word
acceptance_status: passed
created_at: 2026-08-06 11:41:11
updated_at: 2026-08-06 17:17:37
---

# 验收用例

## AC-001 普通业务正文中的 P-word 放行

给定一个已闭环 Issue，其最终状态为完成，关联 Change 已归档。

当该 Issue 子文档正文包含“SKU P-word 图片正式化已完成”这类普通业务描述，并执行 `python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>`。

则 stale scan 不应产生 `issue-subdocument-stale-state` blocker。

## AC-002 结构化状态字段仍严格阻断

给定一个已闭环 Issue，其最终状态为完成，关联 Change 已归档。

当该 Issue 子文档 frontmatter、fenced yaml 或状态表格中残留评审阶段、验收未完成、提案阶段、实现完成但归档未闭环或迭代中等中间态语义。

则 stale scan 必须继续产生 blocker，并给出需要 Workflow Sync/reconcile 或人工修正文案的建议。

## AC-003 流程说明中的待办语义仍严格阻断

给定一个已闭环 Issue 或 Sprint 四件套。

当文档仍包含与真实流程状态冲突的验收、实现、归档或 OpenSpec 执行动作未完成说明。

则 stale scan 必须继续阻断 Sprint archive readiness。

## AC-004 readiness gate 保持一致

给定同一组测试夹具。

当分别执行 `python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>` 与 `python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>`。

则两者对 stale scan 的通过/阻断结果一致，且不会放宽 legacy `openspec/changes/archive/` canonical 引用阻断。

# 回归测试建议

- 在 `tests/test_sprint_close_stale_scan.py` 增加业务正文 `SKU P-word 图片正式化` 放行用例。
- 增加结构化评审中或验收未完成状态残留的阻断用例。
- 保留现有验收未完成、归档未完成、提案阶段、实现完成但归档未闭环、legacy archive path 相关测试。

# 验收结果回填

| 时间 | 结果 | 证据 | 说明 |
|---|---|---|---|
| 2026-08-06 13:08:31 | passed | `pytest tests/test_sprint_close_stale_scan.py`；`scripts/validate-openspec-language.py`；`openspec validate fix-stale-scan-pending-business-word`；`scripts/validate-archive-evidence.py --change fix-stale-scan-pending-business-word --archive-path openspec/archive/2026-08-06-fix-stale-scan-pending-business-word` | 修复已实现并归档；Workflow Sync 已回填验收通过。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: fix-stale-scan-pending-business-word
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

