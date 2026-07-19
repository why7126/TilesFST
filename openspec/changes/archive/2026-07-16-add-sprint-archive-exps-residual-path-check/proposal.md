# Proposal: Sprint 归档与复盘旧路径残留检查

## Why

Sprint 归档会将四件套从 `iterations/change/<sprint-id>/` 迁移到 `iterations/archive/<sprint-id>/`，关联 Change 也会进入 `openspec/changes/archive/<date>-<change-id>/`。当前 `/sprint-archive` 与 `/sprint-exps` 缺少针对旧路径引用的显式残留检查，容易在归档后留下指向 `change/` 或 active Change 目录的旧链接，影响后续追溯与复盘证据可信度。

## What Changes

- 为 `/sprint-archive` 增加归档后路径残留检查，扫描本次 Sprint 关联文档中是否仍引用已迁移的 `iterations/change/<sprint-id>/` 或 active `openspec/changes/<change-id>/` 路径。
- 为 `/sprint-exps` 增加复盘前路径残留检查，若归档 Sprint 的关联文档仍存在旧链接，必须在 Experience Analysis Report 和 evidence hints 中显式提示。
- 新增或扩展脚本能力，以 Sprint scope 为边界生成旧路径残留报告，避免宽泛扫描历史归档或生成物。
- 将检查纳入命令技能与测试，确保成功路径输出摘要、失败路径给出具体文件、旧路径、新路径和建议修正动作。

## Capabilities

### New Capabilities

空。

### Modified Capabilities

- `agent-workflow-tooling`: 增强 Sprint archive / exps 工作流工具的路径一致性门禁，要求归档后关联文档不得残留旧的 `change/` 或 active Change 路径引用。

## Impact

- 影响 `.agents/skills/sprint-archive/SKILL.md`、`.agents/skills/sprint-exps/SKILL.md` 的命令步骤与输出要求。
- 影响 `scripts/` 下 Sprint 归档或 Fact Sheet 相关校验脚本，可能新增专用校验脚本供两个命令复用。
- 影响 `openspec/specs/agent-workflow-tooling/spec.md` 的需求行为。
- 不影响 API、数据库、Web、小程序、管理端权限、Orval 或 Docker Compose 运行配置。
