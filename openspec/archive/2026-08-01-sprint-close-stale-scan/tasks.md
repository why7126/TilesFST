## 1. Stale Scan 脚本

- [x] 1.1 梳理现有 `scripts/archived_path_residuals.py`、`scripts/validate-directory-structure.py`、`scripts/sync-workflow-status.py` 和 `scripts/workflow_sync/**` 中可复用的 Sprint/Change 状态读取逻辑。
- [x] 1.2 新增或扩展 Sprint close stale scan 命令，支持显式 `sprint-xxx` 输入和 `--sprint auto` 解析失败提示。
- [x] 1.3 实现四件套读取边界，仅扫描目标 Sprint 的 `sprint.yaml`、`sprint.md`、`release-note.md`、`acceptance-report.md` 以及由 `sprint.yaml` 指向的必要 Issue/Change 状态证据。
- [x] 1.4 实现中间态文案规则，识别与真实状态冲突的待 `/req-opsx`、待 `/bug-opsx`、待 `/opsx-apply`、`proposed`、`applied` 等 stale 命中。
- [x] 1.5 实现旧归档路径规则，阻断四件套和新生成 Sprint 事实中作为 canonical archive path 的 `openspec/changes/archive/` 引用。
- [x] 1.6 实现报告分级，输出 blocker、warning、allowed_legacy 的命中文件、片段、关联对象、原因和建议修复动作。

## 2. Workflow Sync 与 Sprint Close 接入

- [x] 2.1 调整 Workflow Sync 派生块刷新逻辑，确保机器事实可确定的 Scope 文案不保留过期规划状态。
- [x] 2.2 将 stale scan 接入 `/sprint-archive` 或 Sprint close 相关校验路径，blocker 命中时返回非零退出码。
- [x] 2.3 确保 stale scan 报告明确禁止手工编辑 `sprint.md` workflow-sync marker 派生块，并优先建议重新运行 Workflow Sync 或专用 reconcile。
- [x] 2.4 确保无 blocker 且既有 readiness gate 通过时，Sprint close 流程继续保持原有行为。

## 3. 允许例外与幂等

- [x] 3.1 为测试 fixture、迁移脚本、兼容 fallback、residual scanner 自身 legacy 字符串建立允许例外边界。
- [x] 3.2 确保自动刷新四件套后再次运行 stale scan 不会因同一派生命中重复失败。
- [x] 3.3 确保历史归档 Sprint 文档不会被默认全量扫描或批量改写。

## 4. 测试

- [x] 4.1 新增 pytest fixture，覆盖已创建 Change 后仍提示待 `/req-opsx` 或 `/bug-opsx` 的 blocker。
- [x] 4.2 新增 pytest fixture，覆盖已 apply/archived Change 后仍提示待 `/opsx-apply`、`proposed` 或 `applied` 的 blocker。
- [x] 4.3 新增 pytest fixture，覆盖四件套 canonical archive path 写入 `openspec/changes/archive/` 时的 blocker。
- [x] 4.4 新增测试验证测试 fixture、迁移脚本和兼容读取 helper 中的 legacy 字符串不会阻断 Sprint close。
- [x] 4.5 新增或更新 Workflow Sync 测试，验证刷新派生块后 stale scan 返回 0。
- [x] 4.6 运行聚焦测试：`uv run pytest tests/test_workflow_sync_time_drift.py tests/test_archived_path_residuals.py` 以及新增 stale scan 测试文件。

## 5. 文档与校验

- [x] 5.1 按实现影响更新 `rules/document-governance.md`、`rules/iterations-lifecycle.md`、`rules/directory-structure.md` 或相关 skill 文档中的 Sprint close stale scan 门禁说明。
- [x] 5.2 记录本 Change 不影响 API、数据库、Web、小程序、管理端 UI、Orval 和 Docker Compose。
- [x] 5.3 运行 OpenSpec 校验和目录结构校验，确认 delta spec、Change 文件和禁止目录规则通过。
- [x] 5.4 在 apply/归档前补齐验证记录，包含测试命令、结果摘要和任何无法自动化的人工复核项。

## 验证记录

- `uv run pytest tests/test_sprint_close_stale_scan.py tests/test_sprint_archive_readiness.py`：16 passed。
- `uv run pytest tests/test_workflow_sync_time_drift.py tests/test_archived_path_residuals.py tests/test_sprint_close_stale_scan.py tests/test_sprint_archive_readiness.py`：39 passed。
- `openspec validate sprint-close-stale-scan --strict`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- 本 Change 不影响 API、数据库、Web、小程序、管理端 UI、Orval、Docker Compose、MinIO 上传链路。

## 归档验证摘要

- 验证命令与结果：`uv run pytest tests/test_workflow_sync_time_drift.py tests/test_archived_path_residuals.py tests/test_sprint_close_stale_scan.py tests/test_sprint_archive_readiness.py`，39 passed；`openspec validate sprint-close-stale-scan --strict`，通过；`python scripts/validate-directory-structure.py`，通过。
- 验收结论：通过；Sprint close stale scan CLI、archive readiness 集成、legacy archive path blocker、允许例外和 Workflow Sync 派生幂等相关验收均已覆盖。
- Issue/Sprint 状态：本 Change 为非 REQ/BUG 来源的纯技术治理 Change，未绑定 Issue，未纳入 Sprint；`opsx.apply` 与 `opsx.archive` Workflow Sync 均按 `--sprint auto` 跳过 Sprint artifacts。
- 归档路径与时间：`openspec/archive/2026-08-01-sprint-close-stale-scan/`，归档时间 `2026-08-01 10:31:13`。
