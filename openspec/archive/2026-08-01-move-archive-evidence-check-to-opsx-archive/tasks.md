## 1. Evidence Check Implementation

- [x] 1.1 Extract or reuse a shared archived Change evidence checker for `trace.md` and `## 归档验证摘要` required item validation.
- [x] 1.2 Integrate the evidence checker into the `/opsx-archive` execution path after the canonical archive path is resolved.
- [x] 1.3 Ensure `/opsx-archive` reports evidence status, archive path, checked candidate files, and missing fallback summary items without printing full artifact contents.
- [x] 1.4 Preserve `/sprint-archive` readiness evidence checks as a secondary gate using the same validation rules.

## 2. Skill And Documentation Updates

- [x] 2.1 Update `.agents/skills/opsx-archive/SKILL.md` so archived evidence validation is an explicit final gate for single Change archive.
- [x] 2.2 Update `.agents/skills/sprint-archive/SKILL.md` wording to clarify the check remains a Sprint-level复核, not the first expected detection point.
- [x] 2.3 Record documentation sync outcome; if no long-lived docs need changes, state the reason in the archive output.

## 3. Tests

- [x] 3.1 Add tests for `/opsx-archive` or its archive evidence helper when archived Change contains `trace.md`.
- [x] 3.2 Add tests for archived Change missing `trace.md` but containing a complete `## 归档验证摘要`.
- [x] 3.3 Add tests for archived Change missing both `trace.md` and complete fallback summary, verifying blocker details include Change id, archive path, candidate files, and missing items.
- [x] 3.4 Run existing Sprint readiness tests to confirm secondary gate behavior is unchanged.

## 4. Validation

- [x] 4.1 Run targeted pytest for archive evidence and Sprint readiness coverage.
- [x] 4.2 Run `python scripts/validate-agent-context-budget.py`.
- [x] 4.3 Run `python scripts/validate-directory-structure.py`.
- [x] 4.4 Run `openspec status --change move-archive-evidence-check-to-opsx-archive` and confirm apply requirements are complete.

## 归档验证摘要

- 验证命令与验证结果：`uv run pytest tests/test_archive_change_script.py tests/test_sprint_archive_readiness.py` 通过，12 passed；`python scripts/validate-agent-context-budget.py` 通过；`python scripts/validate-directory-structure.py` 通过；`openspec status --change move-archive-evidence-check-to-opsx-archive` 显示 4/4 artifacts complete。
- 验收结论：通过。`/opsx-archive` 的单 Change archive evidence gate 已前移并由共享 checker、CLI、archive wrapper、Sprint readiness 二次复核和测试覆盖。
- Issue/Sprint 状态：无关联 REQ/BUG；无关联 Sprint，Workflow Sync 对 `opsx.propose` 与 `opsx.apply` 均报告 sprint skipped，原因是该 Change 不在 sprint scope，符合纯技术治理 Change 豁免。
- 归档路径与归档时间：预计归档到 `openspec/archive/2026-08-01-move-archive-evidence-check-to-opsx-archive/`；归档证据摘要写入时间为 `2026-08-01 09:57:54`。
