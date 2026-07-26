## 1. Path Inventory and Migration Plan

- [x] 1.1 盘点仓库内 `openspec/changes/archive`、`openspec/archive`、`archive_dir`、`archive_root`、`resolve_change_file` 等路径引用，输出影响清单。
- [x] 1.2 确认 `openspec/archive/` 目标目录结构和 `<YYYY-MM-DD>-<change-id>` 命名规则。
- [x] 1.3 决定并记录 `openspec/changes/archive/` 迁移后是删除还是仅保留空目录提示。

## 2. Canonical Path Configuration

- [x] 2.1 更新 `openspec/config.yaml`，将 `archive_dir` 指向 `openspec/archive`。
- [x] 2.2 更新 `AGENTS.md` 与 `rules/directory-structure.md` 的 OpenSpec 已完成 Change 目录说明。
- [x] 2.3 更新 `rules/document-governance.md`、`rules/issues-lifecycle.md`、`rules/iterations-lifecycle.md`、`rules/agent-context-budget.md` 中的 Change archive 路径和搜索排除说明。
- [x] 2.4 更新 `.agents/skills/opsx-archive/SKILL.md`、`.agents/skills/openspec-archive-change/SKILL.md`、`.agents/skills/sprint-archive/SKILL.md`、`.agents/skills/sprint-exps/SKILL.md` 及 release 相关技能中的 canonical archive 路径。

## 3. Script and Helper Updates

- [x] 3.1 更新 Workflow Sync Change 收集逻辑，使 archived Change 解析顺序为 active、`openspec/archive`、legacy `openspec/changes/archive`。
- [x] 3.2 更新 Sprint archive readiness、archived path residual、AI usage、Fact Sheet、release 生成和测试 helper 的 archive root 常量或 resolver。
- [x] 3.3 确保新增归档、报告输出和生成事实源只写入 `openspec/archive/`。
- [x] 3.4 对 legacy archive 命中输出 warning 或兼容标记，避免静默继续传播旧路径。

## 4. Historical Directory Migration

- [x] 4.1 将现有 `openspec/changes/archive/<date>-<change-id>/` 目录迁移到 `openspec/archive/<date>-<change-id>/`。
- [x] 4.2 更新 releases、knowledge-base、trace、tasks、tests 中仍应追踪新路径的旧引用。
- [x] 4.3 确认 `openspec/changes/archive/` 不再包含 Change 包目录，并按 1.3 决策删除或保留空提示。
- [x] 4.4 运行路径残留检查，确认新增事实源不再引用 `openspec/changes/archive/` 作为 canonical path。

## 5. Tests and Validation

- [x] 5.1 更新 `tests/path_helpers.py` 和相关 pytest，覆盖 active、canonical archive、legacy archive fallback 三种路径。
- [x] 5.2 更新 Workflow Sync time drift、Sprint archive readiness、archived residual、Fact Sheet、AI usage、release 相关测试期望。
- [x] 5.3 新增或更新测试，确保新增归档和生成报告使用 `openspec/archive/`，并阻止 `openspec/changes/archive/` 新写入。
- [x] 5.4 运行 `openspec validate relocate-openspec-change-archive-root`。
- [x] 5.5 运行相关 pytest：`tests/test_archived_path_residuals.py`、`tests/test_sprint_archive_readiness.py`、`tests/test_workflow_sync_time_drift.py`、`tests/test_generate_sprint_fact_sheet.py` 及受影响的新增测试。
- [x] 5.6 运行 `python scripts/validate-agent-context-budget.py`，确认 archive 搜索排除规则仍符合上下文预算治理。

## 6. Workflow Closure

- [x] 6.1 更新本 Change 的 `trace.md` 或归档验证摘要，记录迁移路径、测试命令和残留检查结果。
- [x] 6.2 运行 `python scripts/sync-workflow-status.py --event opsx.apply --change relocate-openspec-change-archive-root --sprint auto`（若作为纯治理 Change 未纳入 Sprint，输出豁免原因）。
- [x] 6.3 `/opsx-archive relocate-openspec-change-archive-root` 前复核 legacy path 残留、OpenSpec validate、相关 pytest 与 Workflow Sync 状态。
