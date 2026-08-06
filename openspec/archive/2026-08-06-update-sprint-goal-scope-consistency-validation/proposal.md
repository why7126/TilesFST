## 背景

`sprint-020` 已出现机器 Scope 包含 `REQ-0100`，但 `sprint.md`「Sprint 目标编号列表」未列出的漂移。现有 `validate-sprint-scope.py` 只验证 `## 2. Scope` 主表和 Workflow Sync 分组表，因此无法在 `/sprint-propose` 收尾时发现人读目标遗漏。

本变更将 Sprint 目标编号列表纳入 Sprint 规划治理，确保 `sprint.yaml` 机器事实源、`sprint.md` Scope 表和目标编号列表表达同一正式范围。

## 变更内容

- 增强 `scripts/validate-sprint-scope.py`，校验 Sprint 目标编号列表覆盖正式 Scope 中的 REQ、BUG 和策略要求的 Change。
- 更新 `/sprint-propose` 规则，明确追加或修正 Sprint Scope 后必须同步目标编号列表，并在最终校验中覆盖新增项。
- 更新 Workflow Sync 规则边界，明确 `## 2. Scope` 派生表由 Workflow Sync 维护，目标编号列表至少必须由校验兜底发现漂移。
- 增加脚本级回归测试，覆盖 `sprint-020` / `REQ-0100` 漏列场景、完整列表通过场景、短编号与完整 ID 等价场景。

## 能力范围

### 新增能力

无。

### 修改能力

- `sprint-planning-governance`：补充 Sprint 目标编号列表与正式 Scope 的一致性要求。

## 影响

- 影响脚本：`scripts/validate-sprint-scope.py` 及相关测试。
- 影响工作流规则：`.agents/skills/sprint-propose/SKILL.md`、`.agents/skills/workflow-sync/SKILL.md`。
- 影响 Sprint 文档治理：`sprint.md` 的 `## 1. 目标` 与 `## 2. Scope` 一致性。
- 不影响 API、数据库、Web、小程序、管理端运行时代码、Orval、对象存储或 Docker Compose。
